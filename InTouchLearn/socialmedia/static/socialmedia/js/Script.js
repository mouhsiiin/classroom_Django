//.............. ...Start Swiper Story ................
let swiper = new Swiper(".mySwiper",{
    slidesPerView: 5,
    spaceBetween : 5,
});


// ..................Window Scroll.................
window.addEventListener('scroll',()=>{
    document.querySelector('.profile-popup').style.display='none'
    document.querySelector('.add-post-popup').style.display='none'
    document.querySelector('.theme-customize').style.display='none'
});


// .......................Start Aside...................
let menuItem = document.querySelectorAll('.menu-item');
let notificationBox = document.querySelector('.notification-box');

// Active remove..
const removeActive = ()=>{
    menuItem.forEach(item=>{
        item.classList.remove('active')
    })
}

menuItem.forEach(item=>{
    item.addEventListener('click',()=>{
        removeActive();
        item.classList.add('active');
        notificationBox.style.display='none'
    })
});





// ...............Start..Firend Rquestt...............
let Accept = document.querySelectorAll('#Accept');
let Dlete = document.querySelectorAll('#Delete');

Accept.forEach(accept=>{
    accept.addEventListener('click',()=>{
        accept.parentElement.style.display='none'
        accept.parentElement.parentElement.querySelector('.alert').style.display='block'
    })
});
Dlete.forEach(deletee=>{
    deletee.addEventListener('click',()=>{
        deletee.parentElement.parentElement.style.display='none'     
    })
});






//.............. ...Start Profile Popup................
let AllMyProfilePicture = document.querySelectorAll('#my-profile-picture');
let profilePopup = document.querySelector('.profile-popup');
let addPostPopup = document.querySelector('.add-post-popup');
let themeCustomizePopup = document.querySelector('.theme-customize');
let myProfilePictureImg = document.querySelectorAll('#my-profile-picture img');
let ProfileUploader = document.querySelector('#profile-upload');



AllMyProfilePicture.forEach(myProfilePicture=>{
    myProfilePicture.addEventListener('click',()=>{
        profilePopup.style.display='flex'
    })
});


document.querySelectorAll('.close').forEach(AllCloser=>{
    AllCloser.addEventListener('click',()=>{
        profilePopup.style.display='none'
        addPostPopup.style.display='none'
        themeCustomizePopup.style.display='none'
    })
});


ProfileUploader.addEventListener('change', () => {
    const formData = new FormData();
    formData.append('profile_picture', ProfileUploader.files[0]);
    
    fetch('/social/picture_upload', {
        method: 'POST',
        headers: {
            'X-CSRFToken': ProfileUploader.dataset.csrf,
        },
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            }
            else if (response.status === 400) {
                alert('Invalid file type');
            }
            else {
                alert('An error occurred');
            }
        });
    });
    
    


//.................Start Add post Popup................
let createButtonLg = document.querySelectorAll('.creatPostPop');

createButtonLg.forEach(createButton=>{
    createButton.addEventListener('click',()=>{
        addPostPopup.style.display='flex'
    })
});

document.querySelector('#feed-pic-upload').addEventListener('change',()=>{
    document.querySelector('#postIMg').src = URL.createObjectURL(document.querySelector('#feed-pic-upload').files[0]);
});





// ................Mini Button input................
let miniButton = document.querySelector('.mini-button');
let inputPost = document.querySelector('.input-post');



miniButton.addEventListener('click',()=>{
    inputPost.classList.toggle('boxshadow1');
    setTimeout(() => {
        inputPost.classList.remove('boxshadow1');
    }, 3000);
});

miniButton.addEventListener('dblclick',()=>{
    addPostPopup.style.display='flex'
});






// ..............Liked button.............

document.querySelectorAll('.action-button span:first-child i').forEach(liked=>{
    liked.addEventListener('click',()=>{
        liked.classList.toggle('liked');
    })
});


// ......................Theme CustoMize........................
let theme = document.querySelector('.theme-customize')
document.querySelector('#theme').addEventListener('click',()=>{
    console.log('theme')
    theme.style.display='flex'
});

//................... Font Size..................
let fontSize = document.querySelectorAll('.choose-size span');

const removeActiveSelector = ()=>{
    fontSize.forEach(size=>{
        size.classList.remove('active')
    })
}


fontSize.forEach(size=>{
    size.addEventListener('click',()=>{
        let fontSize;
        removeActiveSelector();     
        size.classList.toggle('active'); 
        

        if(size.classList.contains('font-size-1')){
            fontSize = '10px';
        }else if(size.classList.contains('font-size-2')){
            fontSize = '13px';
        }else if(size.classList.contains('font-size-3')){
            fontSize = '16px';
        }else if(size.classList.contains('font-size-4')){
            fontSize = '19px';
        }else if(size.classList.contains('font-size-5')){
            fontSize = '22px';
        }
        // Html root fontsize change...
        document.querySelector('html').style.fontSize = fontSize;
    })
});

//................... Primary Color..................

let colorpallete = document.querySelectorAll('.choose-color span');
var root = document.querySelector(':root');


// remove coloractive........
const removeActiveColor = ()=>{
    colorpallete.forEach(color=>{
        color.classList.remove('active')
    })
}

colorpallete.forEach(color => {
    color.addEventListener('click',()=>{
        let primaryHue;
        removeActiveColor();
        color.classList.add('active');
        
        if(color.classList.contains('color-1')){
            Hue = 252;
        }else if(color.classList.contains('color-2')){
            Hue = 52;
        }else if(color.classList.contains('color-3')){
            Hue = 352;
        }else if(color.classList.contains('color-4')){
            Hue = 152;
        }else if(color.classList.contains('color-5')){
            Hue = 202;
        }
        root.style.setProperty('--primary-color-hue',Hue);
    })    
});



//...................Background Change..................

let bg1 = document.querySelector('.bg1');
let bg2 = document.querySelector('.bg2');

// Theme Background value.....
let darkColorLightTheme;
let lightColorLightTheme;
let whiteColorLightTheme;

const changBg = ()=>{
    root.style.setProperty('--color-dark-light-theme', darkColorLightTheme);
    root.style.setProperty('--color-light-light-theme',lightColorLightTheme);
    root.style.setProperty('--color-white-light-theme', whiteColorLightTheme);
}

bg2.addEventListener('click',()=>{
    darkColorLightTheme = '95%';
    lightColorLightTheme = '5%';
    whiteColorLightTheme = '12%';  

    //Add active class
    bg2.classList.add('active');
    bg1.classList.remove('active');

    bgicon();
    changBg();
});
bg1.addEventListener('click',()=>{
    //Add active class
    bg1.classList.add('active');
    bg2.classList.remove('active');

    window.location.reload();
});




// Dark Theme Aside Icon.....
let menuItemImg = document.querySelectorAll('.menu-item span img');

const bgicon = ()=>{
    menuItemImg.forEach(icon=>{
        icon.classList.add('icon-bg');
    })
}

document.addEventListener('DOMContentLoaded',()=>{
    console.log('loaded')
})

