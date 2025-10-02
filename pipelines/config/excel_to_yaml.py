import os
import pandas as pd
from typing import Optional

# 1) Excel inladen
excel_path = 'etlocal_calculation_rules.xlsx'
xls = pd.ExcelFile(excel_path)

df_etlocal      = pd.read_excel(xls, sheet_name='D_ETLocal_keys_to_ovar')
df_vars         = pd.read_excel(xls, sheet_name='custom_variables')   # eenvoudige bewerkingen
df_funcs        = pd.read_excel(xls, sheet_name='custom_functions')   # max, min, if, iferror
# origin-kolom negeren; we gebruiken alleen kolommen: 
# custom_variables: ['rule_type','variable','origin','element_1'...'element_14','operand_1'...'operand_14']
# custom_functions: ['rule_type','variable','origin','function_name','arg_1','arg_2','arg_3']

def get_elements_and_operands(target_var: str, vars_df: pd.DataFrame):
    """
    Haal voor een ivar de lijsten elements & operands op uit custom_variables.
    - elements: ['ivar1', 'ivar2', ...]
    - operands: ['+', '-', '*', '/', None, ...]
    Raise KeyError als target_var niet in vars_df staat.
    """
    row = vars_df.loc[vars_df['variable'] == target_var]
    if row.empty:
        raise KeyError(f"No basic‐rule for variable '{target_var}'")
    row = row.iloc[0]

    elements = []
    operands = []
    # Maximaal 14 element‐operandparen
    for i in range(1, 15):
        e_col = f'element_{i}'
        o_col = f'operand_{i}'
        elem = row.get(e_col)
        op   = row.get(o_col)

        if isinstance(elem, str) and elem.strip():
            elements.append(elem.strip())
            if isinstance(op, str) and op.strip():
                operands.append(op.strip())
            else:
                operands.append(None)
        # Ook numerieke constants (int/float) toelaten:
        elif isinstance(elem, (int, float)) and not pd.isna(elem):
            elements.append(str(elem))
            if isinstance(op, str) and op.strip():
                operands.append(op.strip())
            else:
                operands.append(None)
        else:
            break

    return elements, operands

def get_function_definition(target_var: str, funcs_df: pd.DataFrame):
    """
    Haal voor een ivar de function_name en argumenten (arg_1, arg_2, arg_3) op uit custom_functions.
    Return een tuple (function_name, [arg_1, arg_2, arg_3_without_nan]).
    Raise KeyError als target_var niet in funcs_df staat.
    """
    # Zoek eerst in variable kolom
    row = funcs_df.loc[funcs_df['variable'] == target_var]
    # Als niet gevonden, zoek in Sector kolom (voor sommige functies staat de naam daar)
    if row.empty:
        row = funcs_df.loc[funcs_df['Sector'] == target_var]
    if row.empty:
        raise KeyError(f"No function‐rule for variable '{target_var}'")
    row = row.iloc[0]

    # Voor rijen waar de variabele naam in Sector staat, gebruik variable kolom voor function_name
    if target_var in funcs_df['Sector'].values and target_var not in funcs_df['variable'].values:
        func_name = row['variable'].strip().lower()
        # Arguments staan dan in function_name en arg_1
        args = []
        for a in ['function_name', 'arg_1', 'arg_2']:
            val = row.get(a)
            if isinstance(val, str) and val.strip():
                args.append(val.strip())
            elif isinstance(val, (int, float)) and not pd.isna(val):
                args.append(str(val))
    else:
        # Normale structuur
        func_name = row['function_name'].strip().lower()
        args = []
        for a in ['arg_1', 'arg_2', 'arg_3']:
            val = row.get(a)
            if isinstance(val, str) and val.strip():
                args.append(val.strip())
            elif isinstance(val, (int, float)) and not pd.isna(val):
                args.append(str(val))

    return func_name, args

def build_ast(components: list, operands: list):
    """
    Bouw (linker‐assoc.) AST voor basic‐expressies:
    - Flatten als alle operators gelijk zijn ('+' of '*').
    Node‐types:
      - leaf:  {'type': 'var',       'name': <ivar>}
      - expr:  {'type': 'expr',      'expression': <sum/minus/...>,
                'left': <subnode>,  'right': <subnode>}
      - flat:  {'type': 'flat',      'expression': <sum/multiply>,
                'components': [<leaf1>, <leaf2>, ...]}
    """
    def op_to_expr(op_sym: str):
        if op_sym == '+': return 'sum'
        if op_sym == '-': return 'minus'
        if op_sym == '*': return 'multiply'
        if op_sym == '/': return 'divide'
        return 'composite'

    n = len(components)
    if n == 0:
        return None

    # 1) Controleer flat‐case (alle '+' of alle '*')
    if n > 1:
        ops_needed = operands[: n - 1]
        unique_ops = set(ops_needed)
        if unique_ops == {'+'}:
            return {
                'type': 'flat',
                'expression': 'sum',
                'components': [{ 'type': 'var', 'name': c } for c in components]
            }
        if unique_ops == {'*'}:
            return {
                'type': 'flat',
                'expression': 'multiply',
                'components': [{ 'type': 'var', 'name': c } for c in components]
            }

    # 2) Controleer of het een alias node is
    if n == 1:
        # Enkel één component: return als leaf node
        return { 'type': 'alias', 'name': components[0] }
    
    # 3) Anders linkser assoc. boom
    node = { 'type': 'var', 'name': components[0] }
    for idx in range(n - 1):
        op_sym = operands[idx]
        right  = { 'type': 'var', 'name': components[idx + 1] }
        expr_name = op_to_expr(op_sym)
        node = {
            'type': 'expr',
            'expression': expr_name,
            'left': node,
            'right': right
        }
    return node

def collect_rules_recursive(var: str, vars_df: pd.DataFrame, funcs_df: pd.DataFrame, collected: dict):
    """
    Verzamel recursief alle benodigde nodes (basic‐AST of function‐node) voor ivar 'var'.
    - collected: dict mapping var → node
    Node‐types:
      - Voor basic‐regel: AST‐structuur zoals build_ast teruggeeft.
      - Voor function‐regel: {'type':'func', 'expression':<func_name>, 'args':[<arg1>,<arg2>,…]}.
    """
    if var in collected:
        return

    # 1) Probeer eerst een basic‐regel
    try:
        elems, ops = get_elements_and_operands(var, vars_df)
        ast_node = build_ast(elems, ops)
        collected[var] = ast_node
        # Recursie voor elk component ivar
        for comp in elems:
            collect_rules_recursive(comp, vars_df, funcs_df, collected)
        return
    except KeyError:
        pass

    # 2) Probeer een function-regel
    try:
        func_name, args = get_function_definition(var, funcs_df)
        # Maak een function-node, maar we gaan args per stuk controleren
        node = {
            'type': 'func',
            'expression': func_name,
            'args': []  # we vullen dit straks met elders AST-structuren of eenvoudige var-namen
        }
        collected[var] = node

        for raw_arg in args:
            # 2a) Kijk of het raw_arg een simpele som/verschil/vermenigvuldiging bevat
            if any(tok in raw_arg for tok in [' + ', ' - ', ' * ', ' / ']):
                # We splitsen op spatie-operator-spatie; aanname: "a - b" (exact deze notatie)
                tokens = raw_arg.split()
                # Eenvoudige parser: [var1, op, var2, op, var3, ...]
                comps = tokens[0::2]    # alle variabelen/constanten
                ops   = tokens[1::2]    # alle operators
                # Bouw een kleine AST voor deze expressie
                nested_ast = build_ast(comps, ops)
                node['args'].append(nested_ast)

                # recursief doorlopen op elke component die wél een ivar is
                for comp_var in comps:
                    if comp_var in vars_df['variable'].values or comp_var in funcs_df['variable'].values:
                        collect_rules_recursive(comp_var, vars_df, funcs_df, collected)

            # 2b) Controleer of het een numerieke constante is
            elif raw_arg.replace('.', '').replace('-', '').isdigit():
                node['args'].append({'type': 'const', 'value': raw_arg})

            # 2c) Anders: behandel als variabele (ook als het niet in Excel sheets staat)
            else:
                # voeg het gewoon toe als leaf-variabele
                node['args'].append({'type': 'var', 'name': raw_arg})
                # recursie op die variabele (alleen als het in Excel sheets staat)
                if raw_arg in vars_df['variable'].values or raw_arg in funcs_df['variable'].values:
                    collect_rules_recursive(raw_arg, vars_df, funcs_df, collected)

        return
    except KeyError:
        pass

    # 3) Geen rule gevonden: treat as leaf‐variable (geen AST node nodig)
    return

def print_ast_node(node: dict, indent: int = 1):
    """
    Print een node in YAML‐stijl, op indent‐niveau:
    - type 'var'  → "- variable: <name>"
    - type 'flat' → "expression: sum/multiply" + list van "- variable: <name>"
    - type 'expr' → genest links/rechts
    - type 'func' → "expression: <func_name>" + list van args (als strings)
    """
    prefix = '  ' * indent

    if node is None:
        return

    t = node.get('type')
    if t == 'var':
        print(f"{prefix}- variable: {node['name']}")
        return

    if t == 'flat':
        expr = node['expression']
        print(f"{prefix}expression: {expr}")
        print(f"{prefix}components:")
        for comp in node['components']:
            print(f"{prefix}  - variable: {comp['name']}")
        return

    if t == 'expr':
        expr = node['expression']
        print(f"{prefix}expression: {expr}")
        print(f"{prefix}components:")
        left = node['left']
        if left['type'] == 'var':
            print(f"{prefix}  - variable: {left['name']}")
        else:
            print(f"{prefix}  -")
            print_ast_node(left, indent + 2)
        right = node['right']
        if right['type'] == 'var':
            print(f"{prefix}  - variable: {right['name']}")
        else:
            print(f"{prefix}  -")
            print_ast_node(right, indent + 2)
        return

    if t == 'func':
        expr = node['expression']
        print(f"{prefix}expression: {expr}")
        print(f"{prefix}components:")
        for arg in node['args']:
            # print argument als losse regel, zonder "variable:" prefix
            print(f"{prefix}  - {arg}")
        return

def print_yaml_for_etlocal_key(etlocal_key: str, df_et: pd.DataFrame,
                              vars_df: pd.DataFrame, funcs_df: pd.DataFrame,
                              output_dir: Optional[str] = None):
    """
    1) Vind de ovar die bij etlocal_key hoort.
    2) Verzamel recursief alle dependencies (basic‐AST & func‐nodes).
    3) Schrijf YAML naar bestand '{output_dir}/{etlocal_key}_dependency.yaml'.
    """
    matches = df_et.loc[df_et['etlocal_key'] == etlocal_key, 'variable']
    if matches.empty:
        raise KeyError(f"ETLocal key '{etlocal_key}' niet gevonden")
    ovar = matches.iloc[0]

    collected = {}
    collect_rules_recursive(ovar, vars_df, funcs_df, collected)

    if output_dir is None:
        out_path = f"{etlocal_key}_dependency.yaml"
    else:
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"{etlocal_key}_dependency.yaml")

    with open(out_path, 'w') as f:
        # Redirect prints naar ons bestand
        def write(line=''):
            f.write(line + '\n')

        # Helper functie om geneste AST te printen
        def file_print_ast(n, indent):
                        p = '  ' * indent
                        if n['type'] == 'var':
                            write(f"{p}- variable: {n['name']}")
                        elif n['type'] == 'flat':
                            write(f"{p}expression: {n['expression']}")
                            write(f"{p}components:")
                            for c2 in n['components']:
                                write(f"{p}  - variable: {c2['name']}")
                        else:  # expr
                            write(f"{p}expression: {n['expression']}")
                            write(f"{p}components:")
                            left2 = n['left']
                            if left2['type'] == 'var':
                                write(f"{p}  - variable: {left2['name']}")
                            else:
                                write(f"{p}  -")
                                file_print_ast(left2, indent + 2)
                            right2 = n['right']
                            if right2['type'] == 'var':
                                write(f"{p}  - variable: {right2['name']}")
                            else:
                                write(f"{p}  -")
                                file_print_ast(right2, indent + 2)

        # Print per verzamelde ivar
        for ivar, node in collected.items():
            write(f"{ivar}:")
            if not(node is None) and node.get('type') == 'alias':
                print
                # Alias node: enkel een variabele, geen verdere details
                write(f"  variable: {node['name']}")
                write("")
                continue
            # Leaf zonder node of type var: basic
            if node is None or node.get('type') == 'var':
                # write("  expression: basic")
                # write("  components: []")
                write(f"  variable: {ivar}")  # geef aan dat het een leaf is die als kolom in de dataframe staat
                write("")
                continue

            t = node['type']
            if t == 'flat':
                write(f"  expression: {node['expression']}")
                write("  components:")
                for comp in node['components']:
                    write(f"    - variable: {comp['name']}")
                write("")
            elif t == 'expr':
                write(f"  expression: {node['expression']}")
                write("  components:")
                left = node['left']
                if left['type'] == 'var':
                    write(f"    - variable: {left['name']}")
                else:
                    write("    -")
                    # geneste indent = 3
                    file_print_ast(left, 3)
                right = node['right']
                if right['type'] == 'var':
                    write(f"    - variable: {right['name']}")
                else:
                    write("    -")
                    file_print_ast(right, 3)
                write("")
            else:  # 'func'
                write(f"  expression: {node['expression']}")
                write("  components:")
                for arg in node['args']:
                    if isinstance(arg, dict) and arg.get('type') == 'var':
                        write(f"    - variable: {arg['name']}")
                    elif isinstance(arg, dict) and arg.get('type') in ['expr','flat']:
                        write("    -")  # we beginnen een genest blok
                        # hergebruik van file_print_ast om nested AST uit te schrijven
                        file_print_ast(arg, indent=3)
                    else:
                        # arg is waarschijnlijk een constante (string of getal)
                        write(f"    - variable: {arg if not isinstance(arg, dict) else arg.get('value')}")
                write("")
        # Tot slot: ETLocal key → ovar
        write(f"{etlocal_key}:")
        write(f"  variable: {ovar}")

def run_for_all_keys(df_et: pd.DataFrame, vars_df: pd.DataFrame,
                     funcs_df: pd.DataFrame, output_dir: str):
    """
    Voor elke etlocal_key in df_et, roep print_yaml_for_etlocal_key aan.
    """
    for etkey in df_et['etlocal_key'].unique():
        try:
            print_yaml_for_etlocal_key(etkey, df_et, vars_df, funcs_df, output_dir)
        except KeyError:
            # Skip keys zonder mapping of regels
            continue

if __name__ == "__main__":
    # Voorbeeld: enkel voor één key
    # single_key = 'input_buildings_electricity_demand'
    # print_yaml_for_etlocal_key(single_key, df_etlocal, df_vars, df_funcs, output_dir=None)

    # Óf: voor alle keys
    run_for_all_keys(df_etlocal, df_vars, df_funcs, output_dir='yaml_files_for_etlocal_key_calculation')