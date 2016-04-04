editor = ace.edit('code_area');
editor.setTheme('ace/theme/monokai');
editor.$blockScrolling=Infinity
editor.setShowPrintMargin(false);

function decode(text){
	text=text.replace(/&#39;/g,"'")			// '/g' added to replace all occurances of the substring else it replaces only first occurance
    text=text.replace(/&quot;/g,'"')
    text=text.replace(/&gt;/g,'>')
    text=text.replace(/&lt;/g,'<')
    return text.replace(/&amp;/g,'&')
}

lang_map={                        // map language values to corresponding files in ace src
	"C":"c_cpp",
	"C++":"c_cpp",
	"C++ 11":"c_cpp",
	"CLOJURE":"clojure",
	"C#":"csharp",
	"JAVA":"java",
	"JAVASCRIPT":"javascript",
	"HASKELL":"haskell",
	"PERL":"perl",
	"PHP":"php",
	"PYTHON":"python",
	"RUBY":"ruby"
}

source_template={
	"C" : "#include <stdio.h>\nint main(void) {\n\t// your code goes here\n\treturn 0;\n}",

	"C++" : "#include <iostream>\nusing namespace std;\n\nint main() {\n\t// your code goes here\n\treturn 0;\n}",

	"C++ 11" : "#include <iostream>\nusing namespace std;\n\nint main() {\n\t// your code goes here\n\treturn 0;\n}",

	"CLOJURE" : "; your code goes here",

	"C#" : "using System;\npublic class Test\n{\n\tpublic static void Main()\n\t{\n\t\t// your code goes here\n\t}\n}",

	"JAVA" : "/* package whatever; // don't place package name! */\n\nimport java.util.*;\nimport java.lang.*;\nimport java.io.*;\n\n\
/* Name of the class has to be \"Main\" only if the class is public. */\nclass Ideone\n{\n\t\
public static void main (String[] args) throws java.lang.Exception\n\t{\n\t\t// your code goes here\n\t}\n}",

	"JAVASCRIPT":"// your code goes here",

	"HASKELL":"main = -- your code goes here",
	
	"PERL":"#!/usr/bin/perl\n# your code goes here",

	"PHP":"<?php\n\n// your code goes here",

	"PYTHON":"# your code goes here",

	"RUBY":"# your code goes here"
}

lang_default=document.getElementById('hiddenlang').innerHTML
document.getElementById("lang").value=lang_default
editor.getSession().setMode("ace/mode/"+lang_map[lang_default])

window.onload=function(){
	if(!document.getElementById('hiddentextarea').innerHTML)	//its a new compilation request page
		{
			editor.focus()
			document.getElementById('status').style.display='none'
			editor.setValue(source_template[lang_default])
			document.getElementById('output').style.display='none'
			document.getElementById('outputtextarea').style.display='none'
		}
	else														//else its output of a code, so focus on the output
		{
			document.getElementById('output').style.display='initial'
			document.getElementById('outputtextarea').style.display='initial'
			document.getElementById('outputtextarea').focus()
			document.getElementById('status').style.display='initial'
			editor.setValue(decode(document.getElementById('hiddentextarea').innerHTML));
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

flag=lang_default		// gives the last selected lang in drop down list
document.getElementById("lang").onchange=function(){
	lang=this.value 		//gives the currect selected lang in drop down list
	//console.log(lang)
	if(decode(document.getElementById('hiddentextarea').innerHTML)==source_template[flag])		//if code == template of last selected lang
		{
			flag=lang
			editor.setValue(source_template[lang])
		}
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
