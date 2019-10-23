builtins.replaceStrings
  [ "\n" ]
  [ "" ]
  (builtins.readFile
    ../src/ekklesia_portal/VERSION)
