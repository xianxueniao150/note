## function


### s
our MarkCodeBlock() function is public, which means that its definition could collide with another public function with the same name. You could make it “private” (local to the script) by prefixing its name with s: in your definition, and with <sid> in your mapping

```
xnoremap m_ :<c-u>call <sid>MarkCodeBlock()<CR>
                       ^^^^^

function! s:MarkCodeBlock()
          ^^
    ...
endfunction
```

### abort
If an error is raised while the statements in your function are being executed, you may want Vim to stop executing the next ones (this gives shorter stack traces). In this case, you can pass the abort argument to :function (see :h :func-abort):

```
function! s:MarkCodeBlock() abort
                            ^^^^^
    ...
endfunction
```



### 函数参数是可变的，内部的改变会影响外部，不想改变的话可以用deepcopy

```vim
function! Sorted(l)
    let new_list = deepcopy(a:l)
    call sort(new_list)
    return new_list
endfunction
```

### Functions as Variables

```
:let Myfunc = function("Append")
:echo Myfunc([1, 2], 3)
```
 Notice that the variable we used started with a capital letter. If a Vimscript variable refers to a function it must start with a capital letter.

Functions can be stored in lists just like any other kind of variable. Run the following commands:

```
:let funcs = [function("Append"), function("Pop")]
:echo funcs[1](['a', 'b', 'c'], 1)
```
 The funcs variable does not need to start with a capital letter because it's storing a list, not a function. The contents of the list don't matter at all.
 
## visual
```
:'<,'>
 ├┘ ├┘
 │  └ mark put automatically on the last line of the visual selection
 └ mark put automatically on the first line of the visual selection (see `:h '<`)
```

So, when :call calls your MarkCodeBlock() function, Vim has automatically prefixed it with a range.
And, from :h func-range:

If [range] is excluded, ":{range}call" will call the function for each line in the range, with the cursor on the start of each line.

Because of this, your function is called once for every line in the range.

You have 2 possibilities:

1. Eliminate the range by making your mapping press C-u (see :h c^u):

	```
	vnoremap <leader>_ :<c-u>call MarkCodeBlock()<CR>
						^^^^^
	```
2. Make Vim know that the function can handle the range itself and doesn't need :call to re-invoke it for every line in the range. You can do so by passing the range argument to :function:

	```
	function! MarkCodeBlock() range
							  ^^^^^
		...
	endfunction
	```

## Paths
```
:echom expand('%:p') " displays the full, absolute path of that file
:echo globpath('.', '*') "display all of the files and directories in the current directory
:echo split(globpath('.', '*'), '\n') "To get a list
:echo split(globpath('.', '*.txt'), '\n') "wildcards
```




