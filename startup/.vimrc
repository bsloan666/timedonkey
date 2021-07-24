autocmd!
set expandtab
set tabstop=4
set shiftwidth=4
set autoindent
set smartindent
set nowrap
set pastetoggle=<F2>
syntax on

function SaveRecord(app, action)
    let com = "echo `date +\"%Y-%m-%d %H:%M:%S\"`," . a:app . "," . a:action . "," . @% . " >> ~/.activitylog"
    call system(com)
    return 0
endfunction

autocmd BufWinEnter * call SaveRecord('vi', 'open')
autocmd BufWritePost * call SaveRecord('vi', 'save')
autocmd BufWinLeave * call SaveRecord('vi', 'close')
