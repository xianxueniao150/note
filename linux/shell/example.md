## 循环curl
```sh
for i in $(seq 10 99) 
	do
	phone="{\"phone\":\"+86150712212$i\"}"
    curl 'https://' \
  --data-raw $phone \
	sleep 1
done
```

