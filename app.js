// ============ APP: loads the menu from the Flask API and drives the 3D viewer ============
var $=function(q,r){return(r||document).querySelector(q)},$$=function(q,r){return[].slice.call((r||document).querySelectorAll(q))};
var MENU=null,BYSLUG={},LS={get:function(k,d){try{var v=JSON.parse(localStorage.getItem(k));return v==null?d:v}catch(e){return d}},set:function(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
var money=function(n){return n?'Rs. '+n.toLocaleString('en-US'):'See menu'};
// ---------- renderer / scene ----------
var R=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});R.setPixelRatio(Math.min(devicePixelRatio||1,2));R.outputEncoding=THREE.sRGBEncoding;R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.05;
var scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(30,1,.1,100);
(function(){try{var pg=new THREE.PMREMGenerator(R),es=new THREE.Scene();es.add(new THREE.Mesh(new THREE.SphereGeometry(40,16,12),new THREE.MeshBasicMaterial({color:0x2a1a12,side:1})));[[0xffffff,-10,12,10,14,8],[0xffe8c0,12,6,8,10,6],[0xffffff,0,16,-8,12,4],[0xff9a70,-14,0,-6,5,12],[0xdfe9ff,0,-6,12,18,3]].forEach(function(a){var m=new THREE.Mesh(new THREE.PlaneGeometry(a[4],a[5]),new THREE.MeshBasicMaterial({color:a[0],side:2}));m.position.set(a[1],a[2],a[3]);m.lookAt(0,0,0);es.add(m)});scene.environment=pg.fromScene(es,.02).texture}catch(e){}})();
scene.add(new THREE.AmbientLight(0x886655,.6));var KL=new THREE.DirectionalLight(0xfff0d8,1.3);KL.position.set(-3,5,7);scene.add(KL);var RL=new THREE.DirectionalLight(0xffb070,.6);RL.position.set(5,2,-4);scene.add(RL);
var ground=new THREE.Mesh(new THREE.CircleGeometry(4.2,64),new THREE.MeshBasicMaterial({color:0x000000,transparent:true,opacity:.28,depthWrite:false}));ground.rotation.x=-Math.PI/2;ground.position.y=-.02;ground.renderOrder=-1;scene.add(ground);
// ---------- viewer state ----------
var S={el:null,slug:null,item:null,obj:null,mode:'item',P:1,play:false,props:[],yaw:0,yawT:0,drag:false,last:0,idle:0,hl:-1,hero:false,hi:0,ht:0,pt:0,labels:[]};
var HERO=['oreo-iced-capp','hazelnut-iced-capp','grilled-chicken-jalapeno','lotus-melt','caramel-iced-macchiato','strawberry-iced-capp','cappuccino','vanilla-dip'];
function disposeObj(o){if(!o)return;scene.remove(o.root);o.root.traverse(function(x){if(x.geometry)x.geometry.dispose&&x.geometry.dispose()})}
function loadItem(slug,hero){var it=BYSLUG[slug];if(!it)return;disposeObj(S.obj);S.props.forEach(function(p){scene.remove(p.g)});S.props=[];$$('.plabel',S.el).forEach(function(l){l.remove()});
 S.slug=slug;S.item=it;S.obj=buildItem(it.model);scene.add(S.obj.root);S.yaw=0;
 var n=it.ingredients.length;it.ingredients.forEach(function(ing,i){var g=makeProp(ing.kind,ing.color);var s=1.15;g.scale.setScalar(s);g.userData.s=s;scene.add(g);var lb=null;if(!hero){lb=document.createElement('div');lb.className='plabel';lb.textContent=ing.name;S.el.appendChild(lb)}S.props.push({g:g,ing:ing,i:i,lb:lb,pos:new THREE.Vector3()})});
 if(!hero){setMode(S.mode)}}
function setMode(m){S.mode=m;S.play=false;if(m==='item')S.P=1;if(m==='ingredients')S.P=0;if(m==='build'){S.P=0;S.play=true}$$('.vmode button').forEach(function(b){b.classList.toggle('on',b.dataset.m===m)});var sl=$('#bslide');if(sl)sl.value=S.P*100}
function fit(){if(!S.el)return;var w=S.el.clientWidth||600,h=S.el.clientHeight||600;R.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()}
function mountStage(el,hero){if(S.el&&S.el!==el){$$('.plabel',S.el).forEach(function(l){l.remove()})}S.el=el;S.hero=!!hero;el.insertBefore(R.domElement,el.firstChild);fit();setTimeout(fit,60)}
addEventListener('resize',fit);
// drag to rotate
document.addEventListener('pointerdown',function(e){if(S.el&&e.target.closest&&e.target.closest('.stage')&&!e.target.closest('.vctl')){S.drag=true;S.lx=e.clientX;S.last=performance.now()}});
addEventListener('pointerup',function(){S.drag=false});
addEventListener('pointermove',function(e){if(S.drag){S.yawT+=(e.clientX-S.lx)*.012;S.lx=e.clientX;S.last=performance.now()}});
// ---------- main loop ----------
var v3=new THREE.Vector3();
function frame(){requestAnimationFrame(frame);if(!S.el||!S.obj)return;var now=performance.now(),dt=Math.min(.05,(now-S.pt)*.001||.016),t=now*.001;S.pt=now;var o=S.obj,it=S.item,n=S.props.length,W2=S.el.clientWidth||1,H2=S.el.clientHeight||1;
 if(S.hero){S.ht+=dt;var cyc=9,u=S.ht%cyc;S.P=clamp01((u-.8)/4.6);if(S.ht>=cyc*(S.hi+1)){S.hi++;loadItem(HERO[S.hi%HERO.length],true);o=S.obj;it=S.item;n=S.props.length}}
 else if(S.mode==='build'&&S.play){S.P=Math.min(1,S.P+dt/7.5);var sl=$('#bslide');if(sl)sl.value=S.P*100;if(S.P>=1)S.play=false}
 var P=S.P,pr={};
 // ingredient props: orbit -> fly into the item as it is built
 var cx=0,cy=o.center,Ro=2.5+o.size*.28;
 S.props.forEach(function(p,i){var s0=i/n*.8,q=S.mode==='ingredients'&&!S.hero?0:clamp01((P-s0)/.24),ang=i/n*Math.PI*2+t*.35;var orb=new THREE.Vector3(Math.cos(ang)*Ro,cy+.35+Math.sin(i*1.7+t*.9)*.35,Math.sin(ang)*Ro);
  var tgt=o.anchor.clone();var e=q*q*(3-2*q);var pos=orb.clone().lerp(tgt,e);pos.y+=Math.sin(q*Math.PI)*1.1;p.g.position.copy(pos);
  var sc=p.g.userData.s*(S.hl===i?1.35:1)*(q>0?Math.max(.02,1-Math.pow(q,2.2)):1);p.g.scale.setScalar(sc);p.g.rotation.y=t*.9+i;p.g.visible=(S.mode==='item'&&!S.hero)?false:(P>=.995&&!S.hero?false:(P<.995||S.mode!=='item'));
  if(S.hero&&P>=.995)p.g.visible=false;
  var r=p.ing.role;pr[r]=Math.max(pr[r]||0,q);p.pos.copy(pos)});
 if(S.mode==='item'&&!S.hero){S.props.forEach(function(p){pr[p.ing.role]=1})}
 pr.lid=clamp01((P-.9)/.1);if(S.mode==='ingredients'&&!S.hero)pr.lid=0;if(S.mode==='item'&&!S.hero)pr.lid=1;
 o.set(pr);
 // camera + rotation
 if(performance.now()-S.last>2500||S.hero){S.yawT+=dt*.5}
 S.yaw+=(S.yawT-S.yaw)*.12;o.root.rotation.set(.28,S.yaw,0);o.root.position.y=Math.sin(t*.8)*.04;
 var d=(o.size*1.65+3.6)*(W2/H2<.9?1.5:1)*(S.mode!=='item'||S.hero?1.35:1);cam.position.set(0,cy*.9+o.size*.15,d);cam.lookAt(0,cy*.9,0);
 ground.visible=true;ground.scale.setScalar(Math.max(.5,o.size*.15));
 // labels
 S.props.forEach(function(p){if(!p.lb)return;var vis=p.g.visible&&S.mode!=='item';p.lb.style.display=vis?'':'none';if(vis){v3.copy(p.pos);v3.y-=.7;v3.project(cam);p.lb.style.transform='translate('+((v3.x*.5+.5)*W2)+'px,'+((-v3.y*.5+.5)*H2)+'px) translate(-50%,0)';p.lb.classList.toggle('on',S.hl===p.i)}});
 R.render(scene,cam)}
function clamp01(x){return Math.max(0,Math.min(1,x))}
frame();
// ---------- thumbnails (progressive, true 3D snapshots) ----------
var thumbQ=[];
function renderThumb(it){var W=420,H=480,keep=[R.domElement.width,R.domElement.height,cam.aspect],o=buildItem(it.model),pr={};it.ingredients.forEach(function(g){pr[g.role]=1});pr.lid=1;o.set(pr);scene.add(o.root);R.setSize(W,H,false);cam.aspect=W/H;cam.updateProjectionMatrix();o.root.rotation.set(.3,.55,0);cam.position.set(0,o.center*.9+o.size*.15,o.size*1.75+3.4);cam.lookAt(0,o.center*.9,0);ground.scale.setScalar(Math.max(.5,o.size*.15));R.render(scene,cam);var url=R.domElement.toDataURL('image/png');scene.remove(o.root);disposeObj(o);fit();return url}
function pumpThumbs(){var n=0;while(thumbQ.length&&n<3){var c=thumbQ.shift(),it=BYSLUG[c.dataset.slug];if(!it||c.dataset.done)continue;var url=renderThumb(it);c.querySelector('img').src=url;c.dataset.done=1;n++}if(thumbQ.length)setTimeout(pumpThumbs,40)}
// ---------- UI ----------
var CAT='all',QRY='';
function card(it){return'<a class="card" href="#/item/'+it.slug+'" data-slug="'+it.slug+'">'+(it.badge?'<span class="badge">'+it.badge+'</span>':'')+'<div class="im"><img alt="'+it.name+' 3D"><div class="sk"></div></div><h3>'+it.name+'</h3><p>'+it.desc+'</p><div class="pr"><b>'+it.priceText+'</b><span>'+it.ingredients.length+' ingredients · view in 3D ›</span></div></a>'}
function renderGrid(){var list=MENU.items.filter(function(i){return(CAT==='all'||i.category===CAT)&&(!QRY||(i.name+' '+i.desc+' '+i.ingredients.map(function(g){return g.name}).join(' ')).toLowerCase().indexOf(QRY)>=0)});
 var g=$('#grid');g.innerHTML=list.length?list.map(card).join(''):'<p class="empty">No items match your search.</p>';thumbQ=$$('.card',g);setTimeout(pumpThumbs,30)}
function renderTabs(){$('#tabs').innerHTML='<button data-c="all" class="on">All ('+MENU.items.length+')</button>'+MENU.categories.map(function(c){return'<button data-c="'+c.slug+'">'+c.name+' ('+MENU.items.filter(function(i){return i.category===c.slug}).length+')</button>'}).join('')}
$('#tabs').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;CAT=b.dataset.c;$$('#tabs button').forEach(function(x){x.classList.toggle('on',x===b)});renderGrid()});
$('#search').addEventListener('input',function(e){QRY=e.target.value.trim().toLowerCase();renderGrid()});
// viewer
function openItem(slug){var it=BYSLUG[slug];if(!it){location.hash='#/';return}var v=$('#viewer');v.classList.add('open');document.body.classList.add('lock');mountStage($('#vstage'),false);S.mode='ingredients';loadItem(slug,false);setMode('build');
 $('#vname').textContent=it.name;$('#vprice').textContent=it.priceText;$('#vdesc').textContent=it.desc;$('#vcat').textContent=(MENU.categories.filter(function(c){return c.slug===it.category})[0]||{}).name;
 $('#vings').innerHTML=it.ingredients.map(function(g,i){return'<li data-i="'+i+'"><i style="background:'+g.color+'"></i><div><b>'+g.name+'</b><span>'+g.info+'</span></div></li>'}).join('');
 var list=MENU.items,idx=list.indexOf(it);$('#vprev').dataset.s=list[(idx+list.length-1)%list.length].slug;$('#vnext').dataset.s=list[(idx+1)%list.length].slug;$('#vadd').dataset.s=slug;document.title=it.name+' – 3D menu'}
function closeViewer(){$('#viewer').classList.remove('open');document.body.classList.remove('lock');mountStage($('#heroStage'),true);S.hero=true;S.hi=0;S.ht=0;loadItem(HERO[0],true);document.title='Tims 3D Menu (concept)'}
$('#vclose').onclick=function(){location.hash='#/'};
$('#vprev').onclick=$('#vnext').onclick=function(e){location.hash='#/item/'+e.currentTarget.dataset.s};
$$('.vmode button').forEach(function(b){b.onclick=function(){setMode(b.dataset.m)}});
$('#bslide').addEventListener('input',function(e){S.play=false;S.mode='build';S.P=e.target.value/100;$$('.vmode button').forEach(function(x){x.classList.toggle('on',x.dataset.m==='build')})});
$('#vings').addEventListener('pointerover',function(e){var li=e.target.closest('li');S.hl=li?+li.dataset.i:-1;$$('#vings li').forEach(function(x){x.classList.toggle('on',x===li)})});
$('#vings').addEventListener('pointerleave',function(){S.hl=-1;$$('#vings li').forEach(function(x){x.classList.remove('on')})});
// cart + order
var cart=LS.get('th_cart',[]);
function saveCart(){LS.set('th_cart',cart);paintCart()}
function paintCart(){var n=cart.reduce(function(a,c){return a+c.qty},0);$('#cartn').textContent=n;var tot=0;$('#cl').innerHTML=cart.length?cart.map(function(c,i){var it=BYSLUG[c.slug];tot+=(it.price||0)*c.qty;return'<div class="ci"><span>'+it.name+'</span><div><button data-d="-1" data-i="'+i+'">−</button> '+c.qty+' <button data-d="1" data-i="'+i+'">+</button></div><b>'+(it.price?money(it.price*c.qty):'—')+'</b></div>'}).join(''):'<p class="empty">Your cart is empty.</p>';$('#ctot').textContent=money(tot)||'—'}
$('#cl').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var i=+b.dataset.i;cart[i].qty+=+b.dataset.d;if(cart[i].qty<1)cart.splice(i,1);saveCart()});
document.addEventListener('click',function(e){var a=e.target.closest('[data-add]');if(a){var s=a.dataset.add,c=cart.filter(function(x){return x.slug===s})[0];if(c)c.qty++;else cart.push({slug:s,qty:1});saveCart();$('#cart').classList.add('open')}});
$('#vadd').onclick=function(){var s=this.dataset.s,c=cart.filter(function(x){return x.slug===s})[0];if(c)c.qty++;else cart.push({slug:s,qty:1});saveCart();$('#cart').classList.add('open')};
$('#cartbtn').onclick=function(){$('#cart').classList.toggle('open')};$('#cclose').onclick=function(){$('#cart').classList.remove('open')};
$('#cform').addEventListener('submit',function(e){e.preventDefault();var f=e.target,msg=$('#cmsg');if(!cart.length){msg.textContent='Add an item first.';return}
 var body={name:f.name.value,phone:f.phone.value,address:f.address.value,notes:f.notes.value,items:cart.map(function(c){return{slug:c.slug,qty:c.qty}})};
 fetch('/api/orders',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){return r.json().then(function(j){return{ok:r.ok,j:j}})}).then(function(x){if(!x.ok){msg.textContent=x.j.error||'Could not place the order.';return}done(x.j.id,x.j.total)}).catch(function(){var id='TH-'+Math.random().toString(36).slice(2,8).toUpperCase(),all=LS.get('th_orders',[]);all.unshift({id:id,body:body});LS.set('th_orders',all);done(id,null)});
 function done(id,total){cart=[];saveCart();f.reset();msg.innerHTML='Order <b>'+id+'</b> received'+(total?' · total '+money(total):'')+'. Thank you!'}});
// router
function route(){var h=location.hash.replace(/^#\/?/,'').split('/');if(h[0]==='item'&&BYSLUG[h[1]])openItem(h[1]);else{if($('#viewer').classList.contains('open'))closeViewer();if(h[0]==='menu'){var m=$('#menu');m&&m.scrollIntoView({behavior:'smooth'})}}}
addEventListener('hashchange',route);
// ---------- boot ----------
function boot(data){MENU=data;MENU.items.forEach(function(i){BYSLUG[i.slug]=i});renderTabs();renderGrid();paintCart();mountStage($('#heroStage'),true);S.hero=true;loadItem(HERO[0],true);route();var l=$('#loader');if(l){l.classList.add('out');setTimeout(function(){l.remove()},900)}}
fetch('/api/menu').then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return window.MENU_FALLBACK}).then(function(d){if(!d){$('#loader').textContent='Could not load the menu.';return}boot(d)});
