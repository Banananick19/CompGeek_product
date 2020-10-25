function comment_text_toggle(button, display) {
    button.nextSibling.style.display = display;
}

let comments = $('.comments-list .comment');

$.each(comments, function(index, elem) {
    let text = elem.querySelector('.comment-text');
    if ( text.textContent.length > 1000 ) {
        let button = document.createElement( "button" );
        button.innerHTML = 'Прочитать длинный комментарии';
        button.classList.add('comment-slide');
        button.classList.add('btn-primary');
        text.insertAdjacentHTML('beforebegin', button.outerHTML);
        text.style.display = 'none';
     }
})
for (let but of document.querySelectorAll('button.comment-slide')) {
    but.onclick = function(e) {
        if ( this.nextSibling.style.display == 'block' ) {
            this.innerHTML = 'Прочитать длинный комментарии';
            comment_text_toggle(this, 'none');
        } else {
            this.innerHTML = 'Закрыть длинный комментарии';
            comment_text_toggle(this, 'block');
        }
    }
};


