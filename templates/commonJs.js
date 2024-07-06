function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}
function myFunction2() {
    document.getElementById("myDropdown2").classList.toggle("show");
}
function myFunction3() {
    document.getElementById("myDropdown3").classList.toggle("show");
}

function myFunctionOut() {
    document.getElementById("myDropdown").classList.toggle("show");
}
function myFunctionOut2() {
    document.getElementById("myDropdown2").classList.toggle("show");
}
function myFunctionOut3() {
    document.getElementById("myDropdown3").classList.toggle("show");
}


// function GoHome() {

//     document.getElementById("top").innerHTML = "Go home?";
// }
// function Home() {

//     document.getElementById("top").innerHTML = "Home";
// }

function loadCommonContent() {
    fetch('/commonHtmlBVES.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('common-content').innerHTML = data;
        })
        .catch(error => console.error('Error loading common content:', error))
}

function loadGoals() {
    document.getElementById("mainBody").innerHTML = 
    `<div  style="top: 25%; position: absolute; width: 100%">
        <div class="wpb_wrapper">
            <p><em><strong>“Our vision is to aid every child in developing clear thinking, social responsibility and self-confidence.”</strong></em></p>
        </div>

        <h2 style="font-size: 22px;line-height: 40px;text-align: left" class="vc_custom_heading" >OUR MISSION</h2>
        <div class="wpb_wrapper" style="width: 40%; float: left; position: relative;">
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;"><strong>Some of the guidelines we follow to keep our mission going are:<strong></span></p>
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To empower every student with vital life skills.</span></p>
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To impart optimism, integrity, and courage.</span></p>
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To unlock and promote hidden talents and potential.</span></p>
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To inculcate a sense of duty towards the family, community, society, nation.</span></p>
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To ignite their interest in the prescribed curriculum through activity.</span></p>
            <p style="background: white; vertical-align: baseline; margin: 0cm 0cm 15.0pt 0cm;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To deliver an educational program that helps them pursue their dream.</span></p>
            <p style="margin: 0cm; margin-bottom: .0001pt; background: white; vertical-align: baseline;"><span lang="EN-US" style="font-family: 'Poppins',serif; color: #333333;">–  To develop moral and ethical values through charitable and volunteer works.</span></p>
        </div>

        <div style="width: 50%; float: right; position: relative;>
                    <div class="vc_single_image-wrapper   vc_box_border_grey"><img width="350" height="350" src="http://www.bluevalleyenglishschool.in/templates/banner/school.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="templates/banner/school.jpeg 350w, templates/banner/school.jpeg 250w" sizes="(max-width: 350px) 100vw, 350px" /></div>
        </div>
    </div>`;
}

function loadCurriculum() {
    document.getElementById("mainBody").innerHTML = 
        `<div  style="top: 25%; position: absolute;">
        <p style="margin: 0cm; margin-bottom: .0001pt; vertical-align: baseline; font-weight: Bold;"><span lang="EN-US">Blue Mountain pre school and Blue Valley English School, Bidkin offers education from kindergarten to grade XII under the CBSE patern. The subjects provided in the primary sections are English, Science, Maths. Hindi, Computer, Social Studies, Environmental Education and Marathi as their compulsory subjects. In the secondary section, English, Science, Maths, Hindi, Computer studies, Social Studies, Environmental Education are compulsory till grade VIII</span></p>
        <p style="margin: 0cm; margin-bottom: .0001pt; vertical-align: baseline;"><span lang="EN-US">At Blue Valley and Blue Mountain, Students also have the option to choose from a vast variety of activities to complement their interests and hone their individual talents. The activities can be broadly categorized into Sports, Music, Dance, Singing etc.</span></p>
        <br><br>
        <h2 style="font-size: 22px;text-align: left" class="vc_custom_heading" >SPORTS</h2><div class="vc_empty_space"   style="height: 32px" ><span class="vc_empty_space_inner"></span>
        <p style="margin: 0cm; margin-bottom: .0001pt; vertical-align: baseline;"><span lang="EN-US">All the physical activities are conducted on their respective playgrounds and courts. The students are supervised and guided by trained sports coaches. The school has outdoor and indoor sports with all equipment made available to students. We encourage students to actively participate in sports for their well being and health.</span></p>
        <br>
        <h2 style="font-size: 22px;text-align: left" class="vc_custom_heading" >MUSIC</h2><div class="vc_empty_space"   style="height: 32px" ><span class="vc_empty_space_inner"></span>
        <p style="margin: 0cm; margin-bottom: .0001pt; vertical-align: baseline;"><span lang="EN-US">Our students are trained under experts who teach them music in the school. The extra facilities provided to students in the music class are training in vocal and instruments. We train them in Classical and Instrumental music and also in Singing</span></p>
        <br>
        <h2 style="font-size: 22px;text-align: left" class="vc_custom_heading" >DANCE</h2>
        <p style="margin: 0cm; margin-bottom: .0001pt; vertical-align: baseline;"><span lang="EN-US">The dance section has a spacious dance hall with trained dance instructor. The students are taught traditional, western as well as fusion forms of dance. In addition the intention is also to keep students fit and agile through the dance session.</span></p>
        <br>
        <h2 style="font-size: 22px;text-align: left" class="vc_custom_heading" >ART</h2>
        <p style="margin: 0cm; margin-bottom: .0001pt; vertical-align: baseline;"><span lang="EN-US">The students of Blue Mountain are trained by qualified art teachers. They are instructed with the basics of sketching, drawing, collage making, colouring, painting and many other art techniques. Exposure to art allows our students to express themselves. The school also teaches the students through hands-on experience in project making and handicrafts.</span></p>
        </div>`;
    }

function loadPrincipal() {
    document.getElementById("mainBody").innerHTML = `
    <div>
        <div style="width: 60%; float: left; position: relative;">
            <h2>MRS. SAVITA TOTALA</h2>
            <p></p>
            <h2><span></span> (Director and Co-Founder)</h2>
            <p><strong><em><b><i>“Our school is a building which has four walls with tomorrow inside.”</i></b></em></strong></p>
            <p>We all want our kids to be successful which is only possible through good and proper education. We at Blue Valley and Blue Mountain believe that our role is to encourage the tiny tots to think and develop as an individual so that they can reach their full potential.</p>
            <br><br><br><br><br><br>
        </div>
        <div style="width: 35%; float: right; position: relative;">
            <div class="vc_single_image-wrapper vc_box_shadow_3d  vc_box_border_grey"><img width="400" height="400" src="/templates/banner/savita.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="/templates/banner/savita.jpeg 400w, /templates/banner/savita.jpeg 150w, /templates/banner/savita.jpeg 300w" sizes="(max-width: 400px) 100vw, 400px" /></div>
            <br><br><br><br>
        </div>
    </div>
    <div>
        <div style="width: 35%; float: left; position: relative;">
            <div class="vc_single_image-wrapper vc_box_shadow_3d  vc_box_border_grey"><img width="400" height="400" src="/templates/banner/satish.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="/templates/banner/satish.jpeg 400w, /templates/banner/satish.jpeg 150w, /templates/banner/satish.jpeg 300w" sizes="(max-width: 400px) 100vw, 400px" /></div>
        </div>
        <div style="width: 60%; right: 5%; float: right; position: relative;">
            <h2>MR. SATISH TOTALA</h2>
            <p></p>
            <h2><span></span> (Chairman and Co-Founder)</h2>
            <p>If we wish to see an enlightened and enterprising nation tomorrow, we must take care to build its future citizens today. Towards this goal, we at Blue Valley and Blue Mountain focus on drawing out and developing the hidden talents of our young ones. We do this by focusing on the education of their minds as well as their hearts to nurture a generation which is well informed and is emotionally stable.</p>
            <br><br><br><br><br><br>
        </div>
    </div>
        `;
}

function loadTeachers() {
    document.getElementById("mainBody").innerHTML = `
    <div>
        <div style="width: 60%; float: left; position: relative;">
            <br><br><br>
            <h2>MRS. VARSHA CHAVAN</h2>
            <p></p>
            <h2><span></span> (VP - Primary)</h2>
            <p><strong><em><b><i>“All odds, challenges, and handicaps of life can be overcome with determination, hard work, insurmountable patience, and tenacity”</i></b></em></strong></p>
            <p>At Blue Valley and Blue Mountain, we relentlessly strive to pursue and maintain academic and co-curricular excellence by nurturing, encouraging and motivating the children in an amicable environment and instil in them a creative passion, resilience and leadership qualities.</p>
            <br><br><br><br><br><br>
        </div>
        <div style="width: 35%; float: right; position: relative;">
            <div class="vc_single_image-wrapper vc_box_shadow_3d  vc_box_border_grey"><img width="400" height="400" src="/templates/banner/varsha.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="/templates/banner/varsha.jpeg 400w, /templates/banner/varsha.jpeg 150w, /templates/banner/varsha.jpeg 300w" sizes="(max-width: 400px) 100vw, 400px" /></div>
            <br><br><br><br>
        </div>
    </div>
    <div>
        <div style="width: 35%; float: left; position: relative;">
            <div class="vc_single_image-wrapper vc_box_shadow_3d  vc_box_border_grey"><img width="400" height="400" src="/templates/banner/harshad.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="/templates/banner/harshad.jpeg 400w, /templates/banner/harshad.jpeg 150w, /templates/banner/harshad.jpeg 300w" sizes="(max-width: 400px) 100vw, 400px" /></div>
            <br><br><br><br>
        </div>
        <div style="width: 60%; right: 5%; float: right; position: relative;">
            <h2>MR. Harshad Devidas</h2>
            <p></p>
            <h2><span></span> (Supervisor Secondary)</h2>
            <p><strong><em><b><i>“What is education? - It is learning.<br>What is learning? - It is thinking.<br>What is thinking? - It is Problem Solving.”</i></b></em></strong></p>
            <p>Education is the whole process of growing up and developement in one's skills. It is the art of shaping the indivisual's personality through physical, emotional, intelluctual and spritual training. Flexibility, Responsibility and Opportunity are the charecteristic features of our school which help the students to learn and grow with new experiences.</p>
            <br><br><br><br><br><br>
        </div>
    </div>
    <div>
        <div style="width: 60%; float: left; position: relative;">
            <h2>MR. KSHAMA TOTALA</h2>
            <p></p>
            <h2><span></span> (Supervisor - PrePrimary)</h2>
            <p>Education is the passport to the future, because tomorrow belongs to those who prepare for it today.  This is applicable for the students of Jr and Sr KG as they prepare themselves for the their time in the school and prepare for the future. We at Blue Valley follow the motto of preparing every student for the future so that when they move to primary school, they will be ready to face the challenges of the evergrowing knowledge.</p>
            <br><br><br><br><br><br>
        </div>
        <div style="width: 35%; float: right; position: relative;">
            <div class="vc_single_image-wrapper vc_box_shadow_3d  vc_box_border_grey"><img width="400" height="400" src="/templates/banner/kshama.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="/templates/banner/kshama.jpeg 400w, /templates/banner/kshama.jpeg 150w, /templates/banner/kshama.jpeg 300w" sizes="(max-width: 400px) 100vw, 400px" /></div>
            <br><br><br><br>
        </div>
    </div>
    <div>
        <div style="width: 35%; float: left; position: relative;">
            <div class="vc_single_image-wrapper vc_box_shadow_3d  vc_box_border_grey"><img width="400" height="400" src="/templates/banner/kavita.jpeg" class="vc_single_image-img attachment-full" alt="" srcset="/templates/banner/kavita.jpeg 400w, /templates/banner/kavita.jpeg 150w, /templates/banner/kavita.jpeg 300w" sizes="(max-width: 400px) 100vw, 400px" /></div>
            <br><br><br><br>
        </div>
        <div style="width: 60%; right: 5%; float: right; position: relative;">
            <h2>MR. SATISH TOTALA</h2>
            <p></p>
            <h2><span></span> (PrePrimary Staff Teacher)</h2>
            <p>One of my favourite poets, William Butler Yeats once said, <strong><em><b><i>“Education is not the filling of a pail, but rather the lighting of a fire.”</i></b></em></strong></p>
            <p>At Blue Valley and Blue Mountain, we see the sparks of this fire in the eyes of our children when they suddenly discover a concept of Physics or Maths or History or Geography which they might have struggled with before while working on a project. It is this joy of recognition and understanding that keeps us at our task long after the last bus has left the school gates. Our commitment to our students extends beyond school hours because what they are exposed to in school has a profound effect on their lives outside the school as well.</p>
            <br><br><br><br><br><br>
        </div>
    </div>
        `;
}