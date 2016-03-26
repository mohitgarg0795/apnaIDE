editor = ace.edit('code_area');
editor.setTheme('ace/theme/monokai');
editor.$blockScrolling=Infinity
editor.setValue(document.getElementById('hiddentextarea').innerHTML);

document.getElementById('body').onload=function(){
	if(!document.getElementById('hiddentextarea').innerHTML)	//its a new compilation request page
		{
			editor.focus()
			document.getElementById('status').style.display='none'
		}
	else														//else its output of a code, so focus on the output
		{
			document.getElementById('output').focus()
			document.getElementById('status').style.display='initial'
		}
}

if(document.getElementById("input").innerHTML)
	{
		document.getElementById("input").style.display='initial'
		document.getElementById("check_input").checked=true
	}

editor.on('change',updatetextarea);
function updatetextarea()
{
	document.getElementById('hiddentextarea').innerHTML=editor.getValue();
}

lang_map={                        // map language values to corresponding files in ace src
	"C":"c_cpp",
	"CPP":"c_cpp",
	"CPP11":"c_cpp",
	"CLOJURE":"clojure",
	"CSHARP":"csharp",
	"JAVA":"java",
	"JAVASCRIPT":"javascript",
	"HASKEL":"haskell",
	"PERL":"perl",
	"PHP":"php",
	"PYTHON":"python",
	"RUBY":"ruby"
}

lang_default=document.getElementById('hiddenlang').innerHTML
document.getElementById("lang").value=lang_default
editor.getSession().setMode("ace/mode/"+lang_map[lang_default])

document.getElementById("lang").onclick=function(){
	lang=this.value
	lang=lang_map[lang]
	editor.getSession().setMode("ace/mode/"+lang)
};

document.getElementById("check_input").onchange=function(){
	flag=this.checked
	if(flag)
		document.getElementById('input').style.display='initial'
	else
		document.getElementById('input').style.display='none'
};

