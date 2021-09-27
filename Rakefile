desc <<-DESC
  Copy-paste the contents of this directory to the public
  etdataset repository.
DESC

task :publish do

  source      = '.'
  destination = '../etdataset-public'
  exclude     = %w[.git corrected_energy_balance_step_1.csv  corrected_energy_balance_step_2.csv energy_balance.csv *autoproducer_table*.* platts.csv odyssee.csv]

  #-------- REMOVE ENTIRE DIRETORY -------------------------------------------

  cmd = "rm -rf #{ destination }/*"

  puts "Executing #{ cmd }"

  %x[ #{ cmd } ]

  #-------- COPY EVERYTHING PRUNED -------------------------------------------

  cmd = ['rsync -rv']

  cmd += exclude.map { |e| "--exclude='#{ e }'" }

  cmd.push source

  cmd.push destination

  %x[ #{ cmd.join(" ") } ]

  puts "Executing #{ cmd.join(" ") }"

  #-------- COPY COMPLETE EXAMPLE DATASET -----------------------------

  cmd2 = "rsync -rv #{ source }/data/example #{ destination }/data"

  puts "Executing #{ cmd2 }"

  %x[ #{ cmd2 } ]

  puts "Done!"
end
