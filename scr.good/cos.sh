

for i in 'Member' ' admin' ; do
	echo $i | egrep "\s.${i}"
done
