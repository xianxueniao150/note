unmarsal时第一个参数不能为空字符串,第二个参数必须为指针
```go
func TestA(t *testing.T) {
	var al []string
	err := json.Unmarshal([]byte(`["aaa"]`), &al)
	if err != nil {
		fmt.Println(err)
	}
}
```

marshal时如果参数为空，最后结果就会为null，unmarsal时也不会报错
```go
func TestA(t *testing.T) {
	var al []string
	datas, err := json.Marshal(al)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(string(datas)) //null
	err = json.Unmarshal(datas, &al)
	if err != nil {
		fmt.Println(err)
	}
}
```

## 特殊字符转义问题

golang json.Marshal方法会把部分字符转为转移字符，从而方便前端的把JSON转为HTML。 也就是说：json.Marshal 默认 escapeHtml 为true,会转义 <、>、&

避免转义
```go
bf := bytes.NewBuffer([]byte{})
jsonEncoder := json.NewEncoder(bf)
jsonEncoder.SetEscapeHTML(false)
jsonEncoder.Encode(rsp)
fmt.Println(bf.String())
```

