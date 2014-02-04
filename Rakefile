desc <<-DESC
  Copy-paste the contents of this directory to the public
  etdataset repository.
DESC

task :publish do

  source      = '.'
  destination = '../etdataset-public'
  exclude     = %w[.git *energy_balance*.* *autoproducer_table*.*]

  #-------- COPY EVERYTHING PRUNED -------------------------------------------

  cmd = ['rsync -rv']

  cmd += exclude.map { |e| "--exclude='#{ e }'" }

  cmd.push source

  cmd.push destination

  exec cmd.join(" ")

  puts "Executing #{ cmd.join(" ") }"

  #-------- COPY COMPLETE EXAMPLE DATASET -----------------------------

  cmd2 = "rsync -rv #{ source }/data/example #{ destination }/data"

  puts "Executing #{ cmd2 }"

  exec cmd2

  puts "Done!"
end
