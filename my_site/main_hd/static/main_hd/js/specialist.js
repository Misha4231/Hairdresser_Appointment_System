let textarea = document.querySelector('.reviews__form-textarea');
console.log(textarea)
textarea.addEventListener("scroll", e => {
    let scHeight = e.target.scrollHeight;
    textarea.style.height = `${scHeight}px`;
});