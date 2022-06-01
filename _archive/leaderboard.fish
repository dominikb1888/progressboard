for name in (gh repo list DB-Teaching -L 500 --json name | jq '.[] | .name'); set user (string split '-' $name); set result (string join " " $user[-1]); echo $result >> results; end
cat results | sort | uniq -c | sort
