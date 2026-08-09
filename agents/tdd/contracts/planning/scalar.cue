package planning

#RepositoryPath: #NonEmptyString & =~"^[^/\\\\]+(/[^/\\\\]+)*$" & !~"(^|/)\\.{1,2}(/|$)"
#SHA256:         string & =~"^[0-9a-f]{64}$"
#SafeInteger:    int & >=-9007199254740991 & <=9007199254740991
