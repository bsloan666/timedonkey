" Put your .vimrc customizations above this line. 


" TimeDonkey vim plugin
function SaveRecord(app, action)
    let com = "echo `date +\"%Y-%m-%d %H:%M:%S\"`," . a:app . "," . a:action . "," . @% . " >> ~/.activitylog"
    call system(com)
    return 0
endfunction

" Events that call TimeDonkey::SaveRecord
autocmd BufWinEnter * call SaveRecord('vi', 'open')
autocmd BufWritePost * call SaveRecord('vi', 'save')
autocmd BufWinLeave * call SaveRecord('vi', 'close')
