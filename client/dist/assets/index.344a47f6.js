import{d as e,p as t,a as n,r as a,c as o,b as i,e as r,w as l,o as s,f as d,g as c,h as u,n as p,t as f,i as m,j as g,F as h,k as v,u as y,l as w,m as x,q as k,s as b,v as A,x as C,y as R,z as T,A as S,B as D,C as N,D as V,E as _,G as L,V as H,H as I}from"./vendor.9b13f05d.js";!function(){const e=document.createElement("link").relList;if(!(e&&e.supports&&e.supports("modulepreload"))){for(const e of document.querySelectorAll('link[rel="modulepreload"]'))t(e);new MutationObserver((e=>{for(const n of e)if("childList"===n.type)for(const e of n.addedNodes)"LINK"===e.tagName&&"modulepreload"===e.rel&&t(e)})).observe(document,{childList:!0,subtree:!0})}function t(e){if(e.ep)return;e.ep=!0;const t=function(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerpolicy&&(t.referrerPolicy=e.referrerpolicy),"use-credentials"===e.crossorigin?t.credentials="include":"anonymous"===e.crossorigin?t.credentials="omit":t.credentials="same-origin",t}(e);fetch(e.href,t)}}();var O=e({name:"Navigation"});t("data-v-2595fee1");const E={class:"bg-gray-700 flex flex-col text-white pt-4 px-8"},P=i("h1",{class:"text-2xl"},"KTrade",-1),M={class:"flex flex-row mt-auto"},U=d("Dashboard"),B=d("Trades"),j=d("Settings");n(),O.render=function(e,t,n,d,c,u){const p=a("router-link");return s(),o("div",E,[P,i("div",M,[r(p,{class:"menu-item",to:"/"},{default:l((()=>[U])),_:1}),r(p,{class:"menu-item",to:"/trades"},{default:l((()=>[B])),_:1}),r(p,{class:"menu-item",to:"/config"},{default:l((()=>[j])),_:1})])])},O.__scopeId="data-v-2595fee1";const G={info:"bg-blue-500",error:"bg-red-500",success:"bg-green-500",warning:"bg-yellow-500"},W={info:"text-blue-500",error:"text-red-500",success:"text-green-500",warning:"text-yellow-500"};var Z=e({props:{notification:{type:Object,required:!0}},setup:({notification:e})=>({colourBoxClasses:c((()=>{let t=["flex","items-center","justify-center","w-12"];return t.push(G[e.type]),t})),titleClasses:c((()=>["font-semibold",W[e.type]]))})});const $={class:"\n      flex\n      w-full\n      max-w-sm\n      mx-auto\n      mt-4\n      overflow-hidden\n      bg-white\n      rounded-lg\n      shadow-md\n    "},q={class:"w-6 h-6 text-white fill-current",viewBox:"0 0 40 40",xmlns:"http://www.w3.org/2000/svg"},z={key:0,d:"M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM16.6667 28.3333L8.33337 20L10.6834 17.65L16.6667 23.6166L29.3167 10.9666L31.6667 13.3333L16.6667 28.3333Z"},F={key:1,d:"M20 3.36667C10.8167 3.36667 3.3667 10.8167 3.3667 20C3.3667 29.1833 10.8167 36.6333 20 36.6333C29.1834 36.6333 36.6334 29.1833 36.6334 20C36.6334 10.8167 29.1834 3.36667 20 3.36667ZM19.1334 33.3333V22.9H13.3334L21.6667 6.66667V17.1H27.25L19.1334 33.3333Z"},K={key:2,d:"M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM21.6667 28.3333H18.3334V25H21.6667V28.3333ZM21.6667 21.6666H18.3334V11.6666H21.6667V21.6666Z"},Y={key:3,d:"M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM21.6667 28.3333H18.3334V25H21.6667V28.3333ZM21.6667 21.6666H18.3334V11.6666H21.6667V21.6666Z"},J={class:"px-4 py-2 -mx-3"},Q={class:"mx-3"},X={class:"text-sm text-gray-600"};Z.render=function(e,t,n,a,r,l){return s(),o("div",$,[i("div",{class:p(e.colourBoxClasses)},[(s(),o("svg",q,["success"===e.notification.type?(s(),o("path",z)):u("",!0),"error"===e.notification.type?(s(),o("path",F)):u("",!0),"info"===e.notification.type?(s(),o("path",K)):u("",!0),"warning"===e.notification.type?(s(),o("path",Y)):u("",!0)]))],2),i("div",J,[i("div",Q,[i("span",{class:p(e.titleClasses)},f(e.notification.title),3),i("p",X,f(e.notification.text),1)])])])};var ee=e({components:{AppNotification:Z}});const te={class:"\n        fixed\n        inset-0\n        flex\n        items-start\n        justify-end\n        p-6\n        px-4\n        py-6\n        pointer-events-none\n        z-10\n      "},ne={class:"w-full max-w-sm"};ee.render=function(e,t,n,d,c,u){const p=a("app-notification"),f=a("Notification"),v=a("NotificationGroup");return s(),m(v,{group:"notifications"},{default:l((()=>[i("div",te,[i("div",ne,[r(f,{enter:"transform ease-out duration-300 transition","enter-from":"translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4","enter-to":"translate-y-0 opacity-100 sm:translate-x-0",leave:"transition ease-in duration-500","leave-from":"opacity-100","leave-to":"opacity-0",move:"transition duration-500","move-delay":"delay-300"},{default:l((({notifications:e})=>[(s(!0),o(h,null,g(e,(e=>(s(),m(p,{key:e.id,notification:e},null,8,["notification"])))),128))])),_:1})])])])),_:1})};var ae=e({components:{Navigation:O,AppNotifications:ee},name:"App",sockets:{info({message:e}){v({group:"notifications",title:"Info",text:e,type:"info"},5e3)},warning({message:e}){v({group:"notifications",title:"Warning",text:e,type:"warning"},5e3)},error({message:e}){v({group:"notifications",title:"Error",text:e,type:"error"},5e3)},success({message:e}){v({group:"notifications",title:"Success",text:e,type:"success"},5e3)}},setup(e,t){const n=y();return{isSetup:c((()=>"Setup"===n.name))}}});const oe={class:"ktrade bg-gray-200 overflow-auto flex flex-col"},ie={class:"flex-1 p-8"};ae.render=function(e,t,n,l,d,c){const p=a("navigation"),f=a("app-notifications"),g=a("router-view");return s(),o("div",oe,[e.isSetup?u("",!0):(s(),m(p,{key:0,class:"flex-initial"})),r(f),i("div",ie,[r(g)])])};var re=e({name:"Input",props:{label:{type:String,required:!0},description:{type:String,required:!1,default:null},modelValue:{type:[String,Number],required:!1,default:null}},setup:(e,{emit:t})=>({onInput:e=>{const n=e.target.value;t("update:modelValue",n)}})});const le={class:"flex flex-col mb-4"},se={class:"text-lg"},de={key:0,class:"text-sm mb-2"},ce=["value"];re.render=function(e,t,n,a,r,l){return s(),o("div",le,[i("label",se,f(e.label),1),e.description?(s(),o("span",de,f(e.description),1)):u("",!0),i("input",{class:"border border-gray-400 p-2 rounded",value:e.modelValue,type:"text",onInput:t[0]||(t[0]=(...t)=>e.onInput&&e.onInput(...t))},null,40,ce)])};var ue=e({name:"Button"});const pe={class:"\n      rounded rounded\n      bg-blue-500\n      hover:bg-blue-600\n      text-white\n      px-2\n      py-1\n      cursor-pointer\n      inline-block\n    "};ue.render=function(e,t,n,a,i,r){return s(),o("div",pe,[w(e.$slots,"default")])};var fe=e({name:"Header"});const me={class:"text-xl mb-8"};fe.render=function(e,t,n,a,i,r){return s(),o("h2",me,[w(e.$slots,"default")])};const ge={getRowNodeId:e=>e.id},he=k(),ve=k(),ye=k({}),we=(e,t)=>{var n;"UNWATCH"===e?(n=t,confirm("Are you sure?")?x.post("/unwatch",{id:n.id}).then((({data:e})=>e)):Promise.reject()).then((()=>{var e;null==(e=null==he?void 0:he.value)||e.applyTransaction({remove:[t]}),v({group:"notifications",title:"Success",text:`${t.ticker} was successfully unwatched`},2e3)})):"BUY"===e&&(e=>{x.post("/trades",{watched_ticker_id:e.id}).then((({data:e})=>e))})(t)},xe=[{field:"ticker",headerName:"Ticker"},{field:"price",headerName:"Price",enableCellChangeFlash:!0},{field:"adr",headerName:"ADR"},{field:"low",headerName:"LOD"},{field:"high",headerName:"HOD"},{field:"actions",headerName:"Actions",cellRenderer:"ActionsCellRenderer",cellRendererParams:{click(e,t){we(e,t)}}}],ke=e=>{he.value=e.api,ve.value=e.columnApi,he.value.setRowData(Object.values(ye.value))};var be=e({name:"Panel"});const Ae={class:"bg-white border border-gray-300 rounded-lg"};be.render=function(e,t,n,a,i,r){return s(),o("div",Ae,[w(e.$slots,"default")])};var Ce=e({components:{AppButton:ue},props:["params"],methods:{clicked(e){this.params.click(e,this.params.data)}}});const Re={class:"flex flex-row"},Te=d("Buy"),Se=d("Unwatch");Ce.render=function(e,t,n,i,d,c){const u=a("app-button");return s(),o("div",Re,[r(u,{onClick:t[0]||(t[0]=t=>e.clicked("BUY"))},{default:l((()=>[Te])),_:1}),r(u,{onClick:t[1]||(t[1]=t=>e.clicked("UNWATCH"))},{default:l((()=>[Se])),_:1})])};var De=e({components:{ActionsCellRenderer:Ce,AgGridVue:b.AgGridVue,AppInput:re,AppButton:ue,AppHeader:fe,AppPanel:be},sockets:{tickerUpdated({watched_ticker_id:e,field:t,value:n}){var a,o;let i=null==(a=this.gridApi.getRowNode(e.toString()))?void 0:a.data;i&&(i[t]=n,null==(o=this.gridApi)||o.applyTransactionAsync({update:[i]}))}},setup(){const e=k("");return A((async()=>{await x.get("/watches").then((({data:e})=>{e.forEach((e=>{ye.value[e.id]=e})),he.value&&he.value.setRowData(e)}))})),{addTicker:()=>{x.post("/watch",{ticker:e.value}).then((({data:e})=>{var t;null==(t=he.value)||t.applyTransaction({add:[e]})})).catch((e=>{var t,n,a;(null==(n=null==(t=e.response)?void 0:t.data)?void 0:n.error)?alert(null==(a=e.response)?void 0:a.data.error):(alert("Unexpected error occurred"),console.log(e))}))},newTicker:e,columnDefs:xe,rowActionClicked:we,rowData:ye,gridApi:he,colApi:ve,gridOptions:ge,gridReady:ke}}});const Ne={class:"flex flex-col h-full"},Ve={class:"w-64"},_e=d("Add");De.render=function(e,t,n,d,c,u){const p=a("ag-grid-vue"),f=a("app-panel"),m=a("app-input"),g=a("app-button");return s(),o("div",Ne,[r(f,{class:"overflow-hidden flex-1"},{default:l((()=>[r(p,{class:"h-full w-full ag-theme-alpine",columnDefs:e.columnDefs,gridOptions:e.gridOptions,onGridReady:e.gridReady},null,8,["columnDefs","gridOptions","onGridReady"])])),_:1}),r(f,{class:"p-8 mt-4 flex-initial"},{default:l((()=>[i("div",Ve,[r(m,{modelValue:e.newTicker,"onUpdate:modelValue":t[0]||(t[0]=t=>e.newTicker=t),label:"Watch a new ticker"},null,8,["modelValue"]),r(g,{onClick:e.addTicker},{default:l((()=>[_e])),_:1},8,["onClick"])])])),_:1})])};const Le=e=>{var t,n,a;throw x.isAxiosError(e)&&(null==(n=null==(t=e.response)?void 0:t.data)?void 0:n.error)?alert(null==(a=e.response)?void 0:a.data.error):alert("Unexpected error occurred"),e},He={getRowNodeId:e=>e.orderId},Ie=k(),Oe=k(),Ee=k({}),Pe=(e,t)=>{switch(e){case"SELL":break;case"TRIM_THIRD":case"TRIM_HALF":((e,t)=>{x.post("/trim",{trade:e.id,amount:t}).then((({data:e})=>e)).then((()=>{v({group:"notifications",title:"Pending",text:`Requested sell of 1/3 of ${e.ticker}`},2e3)})).catch(Le)})(t,"TRIM_THIRD"===e?"THIRD":"HALF");break;case"CLOSE":case"CANCEL":(e=>{x.post(`/trades/${e.id}/close`).then((()=>{v({group:"notifications",title:"Placed SELL order",text:"A SELL order was placed to close this position"})})).catch(Le)})(t);break;case"DELETE":(e=>x.delete(`/trades/${e.id}`).then((()=>{v({group:"notifications",title:"Deleted",text:"The trade was successfully deleted"})})).catch(Le))(t).then((()=>{var e;null==(e=Ie.value)||e.applyTransaction({remove:[t]})}))}},Me=[{field:"ticker",headerName:"Ticker"},{field:"orderStatus",headerName:"Status"},{field:"orderStatusDesc",headerName:"Desc",flex:1},{field:"currentPositionSize",headerName:"Current position"},{field:"filled",headerName:"Filled"},{field:"priceAtOrder",headerName:"Price when ordered"},{field:"orderedAt",headerName:"Ordered at"},{field:"actions",headerName:"",cellClass:"actions",pinned:"right",width:65,cellStyle:()=>({padding:"0"}),cellRenderer:"ActionsCellRenderer",cellRendererParams:{click(e,t){Pe(e,t)}}}],Ue=e=>{Ie.value=e.api,Oe.value=e.columnApi,Ie.value.setRowData(Object.values(Ee.value))};var Be=e({name:"Dropdown",directives:{clickAway:C},props:{options:{type:Array,required:!0}},emits:["option-clicked"],setup(){let e=k(!1);return{isOpen:e,closeDropdown:()=>e.value=!1,openDropdown:()=>e.value=!0}}});const je={key:1,class:"\n      origin-top-right\n      absolute\n      right-0\n      mt-2\n      w-56\n      rounded-md\n      shadow-lg\n      bg-white\n      ring-1 ring-black ring-opacity-5\n      divide-y divide-gray-100\n      focus:outline-none\n    ",role:"menu","aria-orientation":"vertical","aria-labelledby":"menu-button",tabindex:"-1"},Ge=["onClick"];Be.render=function(e,t,n,a,i,r){const l=R("click-away");return e.isOpen?T((s(),o("div",je,[(s(!0),o(h,null,g(e.options,((t,n)=>(s(),o("div",{key:n,class:"py-1",role:"none"},[(s(!0),o(h,null,g(t,((t,n)=>(s(),o("a",{key:n,href:"#",class:"text-gray-700 block px-4 py-2 text-sm",role:"menuitem",tabindex:"-1",onClick:S((n=>e.$emit("option-clicked",t)),["prevent"])},f(t.label),9,Ge)))),128))])))),128))],512)),[[l,e.closeDropdown]]):w(e.$slots,"trigger",{key:0,open:e.openDropdown})};var We=e({components:{AppButton:ue,AppDropdown:Be},props:{params:{type:Object,required:!1}},setup:()=>({actions:k([])}),mounted(){"complete"===this.params.data.orderStatus?this.actions.push([{label:"Trim 1/3",action:"TRIM_THIRD"},{label:"Trim 1/2",action:"TRIM_HALF"},{label:"Close",action:"CLOSE"}]):this.actions.push([{label:"Cancel order",action:"CANCEL"}]),this.actions.push([{label:"Delete",action:"DELETE",confirm:"Are you sure you want to delete this trade? Deleting an open trade will keep the position open."}])},methods:{optionClicked(e){if(e.confirm){if(!confirm(e.confirm))return}this.params.click(e.action,this.params.data)}}});const Ze={class:"flex flex-row h-full items-center"},$e=d("Actions");We.render=function(e,t,n,i,d,c){const u=a("app-button"),p=a("app-dropdown");return s(),o("div",Ze,[r(p,{class:"w-full h-full flex flex-col justify-center",options:e.actions,onOptionClicked:e.optionClicked},{trigger:l((({open:e})=>[r(u,{onClick:e},{default:l((()=>[$e])),_:2},1032,["onClick"])])),_:1},8,["options","onOptionClicked"])])};var qe=e({components:{ActionsCellRenderer:We,AgGridVue:b.AgGridVue,AppInput:re,AppButton:ue,AppHeader:fe,AppPanel:be},sockets:{tradeFilled({order_id:e,amount:t}){var n,a;let o=null==(n=this.gridApi.getRowNode(e.toString()))?void 0:n.data;o&&(o.filled+=t,o.currentPositionSize+=t,null==(a=this.gridApi)||a.applyTransactionAsync({update:[o]}))},tradeSold({order_id:e,amount:t}){var n,a;let o=null==(n=this.gridApi.getRowNode(e.toString()))?void 0:n.data;o&&(o.currentPositionSize-=t,null==(a=this.gridApi)||a.applyTransactionAsync({update:[o]}))},tradeStatus({order_id:e,status:t,description:n}){var a,o;let i=null==(a=this.gridApi.getRowNode(e.toString()))?void 0:a.data;i&&(i.orderStatus=t,i.orderStatusDesc=n,null==(o=this.gridApi)||o.applyTransactionAsync({update:[i]}))}},setup:()=>(A((async()=>{await x.get("/trades").then((({data:e})=>{e.forEach((e=>{Ee.value[e.orderId]=e})),Ie.value&&Ie.value.setRowData(e)}))})),{columnDefs:Me,rowActionClicked:Pe,rowData:Ee,gridApi:Ie,colApi:Oe,gridOptions:He,gridReady:Ue})});const ze={class:"flex flex-col h-full"};qe.render=function(e,t,n,i,d,c){const u=a("ag-grid-vue"),p=a("app-panel");return s(),o("div",ze,[r(p,{class:"overflow-hidden flex-1"},{default:l((()=>[r(u,{class:"h-full w-full ag-theme-alpine",columnDefs:e.columnDefs,gridOptions:e.gridOptions,onGridReady:e.gridReady},null,8,["columnDefs","gridOptions","onGridReady"])])),_:1})])};var Fe=e({});const Ke={class:"config"},Ye=[i("p",null,"Config",-1)];Fe.render=function(e,t,n,a,i,r){return s(),o("div",Ke,Ye)};var Je=e({components:{AppButton:ue,AppHeader:fe,AppInput:re,AppPanel:be},setup:()=>({config:k({maxRisk:.5,maxSize:33,twsHost:"localhost",twsPort:4e3})}),methods:{submit(){x.post("/configure",this.config).then((()=>{this.$router.replace("/")})).catch((e=>{alert("Error")}))}}});const Qe={class:"config flex justify-center"},Xe=d("Welcome to KTrade"),et=i("p",{class:"mb-8"}," Lets get setup. Fill in the details below and we can get started ",-1),tt=d("Continue");Je.render=function(e,t,n,i,d,c){const u=a("app-header"),p=a("app-input"),f=a("app-button"),m=a("app-panel");return s(),o("div",Qe,[r(m,{class:"w-1/2"},{default:l((()=>[r(u,null,{default:l((()=>[Xe])),_:1}),et,r(p,{modelValue:e.config.maxRisk,"onUpdate:modelValue":t[0]||(t[0]=t=>e.config.maxRisk=t),label:"Max risk",description:"Your % maximum risk per trade"},null,8,["modelValue"]),r(p,{modelValue:e.config.maxSize,"onUpdate:modelValue":t[1]||(t[1]=t=>e.config.maxSize=t),label:"Max trade size",description:"The maximum % of your account per trade"},null,8,["modelValue"]),r(p,{modelValue:e.config.twsHost,"onUpdate:modelValue":t[2]||(t[2]=t=>e.config.twsHost=t),label:"TWS hostname",description:"Where is TWS currently running (e.g localhost)"},null,8,["modelValue"]),r(p,{modelValue:e.config.twsPort,"onUpdate:modelValue":t[3]||(t[3]=t=>e.config.twsPort=t),label:"TWS port",description:"The port that the TWS API is running on"},null,8,["modelValue"]),r(f,{onClick:e.submit},{default:l((()=>[tt])),_:1},8,["onClick"])])),_:1})])};const nt=[{path:"/",name:"Dashboard",component:De},{path:"/trades",name:"Trades",component:qe},{path:"/config",name:"Config",component:Fe},{path:"/initial_setup",name:"Setup",component:Je}],at=D({history:N("/"),routes:nt}),ot=V({state:()=>({}),mutations:{},actions:{SOCKET_TICKER_UPDATE(e){console.log(e)}}});x.defaults.baseURL="http://localhost:5000";const it=_(ae);it.use(at),it.use(ot),it.use(L),it.use(new H({debug:!0,connection:I("http://localhost:5000",{path:"/socket.io"})})),at.isReady().then((()=>{it.mount("#app")}));
