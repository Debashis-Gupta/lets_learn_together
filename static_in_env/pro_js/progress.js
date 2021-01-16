var skills =['.ht','.cs','.jq','.js','.ph','.lar',
'.fl','.dj','.ut','.pt',
'.tk','.tr','.ba','.aa',
'.py','.cpp','.bd',
'.lin','.win',
'.gd','.gs','.gsp','.git'
]

function animate() {
    skills.forEach(items=>{
        let btn = document.querySelector(items);
        btn.style.width = btn.getAttribute("data-attr") + '%';
        btn.style.transition='3s';
    })
    setTimeout(animate, 1000);
      
}

animate();













// var skills = {
//     ht: 75,
//     jq: 25,
//     sk: 90,
//     ph: 75,
//     il: 90,
//     in: 85,
//     pl: 75
//   };
  
//   $.each(skills, function(key, value) {
//     var skillbar = $('.' + key);
    
//     skillbar.animate(
//     {
//       width: value + "%",
//       duration:1000,
//       delay:10,
//       iteration:Infinity,
//     },
   
//     // function() {
//     //   $(".speech-bubble").fadeIn();
//     // }
//     );
//   });