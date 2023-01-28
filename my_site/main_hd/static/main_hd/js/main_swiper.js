new Swiper('.image-slider',{
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
        dynamicBullets: true,
    },
    autoplay: {
        delay: 1500,
        stopOnLastSlide: false,
        disableOnInteravtion: false
    },
    loop: true,

});

//const animItems = document.querySelectorAll('._anim-items');
//if(animItems.length>0){
//    window.addEventListener('scroll', animOnScroll);
//    function animOnScroll(){
//        for(let index = 0; index<animItems.length; index++){
//            const animItem = animItems[index];
//            const animItemHeight = animItem.offsetHeight;
//            const animItemOffset = offset(animItem).top;
//            const animStart = 4;
//
//            let animItemPoint = window.innerHeight - animItemHeight / animStart;
//
//            if(animItemHight > window.innerHeight){
//                animItemPoint = window.innerHeight - window.innerHeight / animStart;
//            }
//
//            if((pageYOffset > animItemOffset - animItemPoint) && pageYOffset < (animItemOffset + animItemHeight)){
//                animItem.classList.add('_active');
//            }
//            else{
//                animItem.classList.remove('_active');
//            }
//        }
//    }
//    function offset(el){
//        const rect = el.getBoudingClientRect(),
//            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
//            scrollTop = window.pageYOffset || document.documentElement.scrollTop;
//        return {top: rect.top + scrollTop, left: rect.left + scrollLeft}
//    }
//}