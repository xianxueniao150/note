## 表格标题鼠标浮动显示注释
```js
{
  value: 'trial',
  label: '是否为试用VIP',
  formatter: row => {
	return this.trialMap.get(row.vip_info.free_trial)
  },
  renderHeaderMethod: (h, { column }) => {
	return h('div', [
	  h('span', column.label),
	  h(
		'el-tooltip',
		{
		  props: {
			effect: 'dark',
			content: '当用户角色为付费用户时，该属性表明此VIP是试用还是正式；当用户角色为普通用户时，忽略该属性',
			placement: 'top'
		  }
		},
		[
		  h('i', {
			class: 'el-icon-question',
			style: 'color:#409EFF;margin-left:5px;'
		  })
	   ]
	  )
	])
  }
}, 
```
