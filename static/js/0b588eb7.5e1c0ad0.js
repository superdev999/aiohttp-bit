(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["0b588eb7"],{1445:function(t,e,s){"use strict";var o=s("fd5d"),n=s.n(o);n.a},c0d6:function(t,e,s){"use strict";s.r(e);var o=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"flex flex-center",staticStyle:{"padding-top":"150px"}},[s("div",{staticClass:"q-pa-md q-gutter-md"},[s("q-card",{staticClass:"login"},[s("q-card-section",[s("div",{staticClass:"form-group top-right-control"},[t.isConnected?t._e():s("q-icon",{staticClass:"disconnected",staticStyle:{"font-size":"22px"},attrs:{name:"error"}}),t.isConnected?s("q-icon",{staticClass:"connected",staticStyle:{"font-size":"22px"},attrs:{name:"swap_vertical_circle"}}):t._e()],1)]),t.showMsgLog?t._e():s("q-card-section",[s("q-splitter",{staticStyle:{height:"500px"},attrs:{limits:[50,50]},scopedSlots:t._u([{key:"before",fn:function(){return[s("div",{staticClass:"q-pa-md"},[s("div",{staticClass:"text-h4 q-mb-md"},[t._v("Wallet info")]),s("div",{staticClass:"q-my-md"},[s("pre",[t._v(t._s(t.wallet))])])])]},proxy:!0},{key:"after",fn:function(){return[s("div",{staticClass:"q-pa-md"},[s("div",{staticClass:"text-h4 q-mb-md"},[t._v("Network stats")]),s("div",{staticClass:"q-my-md"},[t._v(t._s(t.network))])])]},proxy:!0}],null,!1,1272577227),model:{value:t.splitterModel,callback:function(e){t.splitterModel=e},expression:"splitterModel"}})],1),t.showMsgLog?s("q-card-section",[s("q-virtual-scroll",{staticStyle:{"max-height":"500px"},attrs:{items:t.messages,separator:""},scopedSlots:t._u([{key:"default",fn:function(e){var o=e.item,n=e.index;return[s("q-item",{key:n,attrs:{dense:""}},[s("q-item-section",[s("q-item-label",[t._v("\n                  "+t._s(o.date)+" - "+t._s(o.message)+"\n                ")])],1)],1)]}}],null,!1,2171557874)})],1):t._e(),s("q-card-actions",[s("q-btn",{attrs:{flat:""},on:{click:t.showlog}},[t._v("Show log")])],1)],1)],1)])},n=[],i={name:"PageIndex",data:function(){return{showMsgLog:!1,splitterModel:50}},computed:{isConnected:function(){return this.$store.getters["Socket/getConnectedStatus"]},wallet:function(){return this.$store.getters["Socket/getWallet"]},network:function(){return this.$store.getters["Socket/getNetwork"]},messages:function(){return this.$store.getters["Socket/getMessages"]}},methods:{showlog:function(){console.log("showlog."),this.showMsgLog=!this.showMsgLog}}},a=i,c=(s("1445"),s("a6c2")),r=Object(c["a"])(a,o,n,!1,null,"cc7ebe8c",null);e["default"]=r.exports},fd5d:function(t,e,s){}}]);