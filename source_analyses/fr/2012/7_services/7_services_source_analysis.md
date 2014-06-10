# 7. Services analysis

The dashboard assumptions for the first attempt were obtained from the NL 2011 dataset.


The following changes were made:

- A first estimation of the final demand is made proportional to the application split in the NL 2011 dataset.
- A rough estimate of the final demand for space heating is made based on the Odyssee 2011 data. The 2011 values are scaled to the final demand in 2012 taken from the IEA energy balance.
- A rough estimate of the useful heat delivered by the remaining technologies is made based on Odyssee 2011 data.
- Increased the technology share of electric heaters in space heating to 30% and adapt the share of gas-fired heaters to make it 100% to avoid negative final demand used for non-electric other appliances.


Issues:

- The application split (final demand) and technology shares requires research.
- Demand for other carriers is appr. 12 PJ. This energy use is not accounted for in the ETM.
