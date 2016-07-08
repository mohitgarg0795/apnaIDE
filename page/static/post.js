editor = ace.edit('code_area');
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
theme_default=document.getElementById('hiddentheme').innerHTML

editor.setTheme('ace/theme/'+theme_default);
document.getElementById("lang").value=lang_default
document.getElementById("theme").value=theme_default
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
			if(document.getElementById('outputtextarea').innerHTML!=''){
				document.getElementById('output').style.display='initial'
				document.getElementById('outputtextarea').style.display='initial'
				document.getElementById('output_focus').scrollIntoView()
			}
			else
				document.getElementById('status_focus').scrollIntoView()
			document.getElementById('status').style.display='initial'
			editor.setValue(decode(document.getElementById('hiddentextarea').innerHTML));
		}
}

temp_input=''
function input_check()
{
	flag=document.getElementById("check_input").checked
	if(flag){
		document.getElementById('code_area').style.width='73%'
		document.getElementById('input').style.display='initial';
		document.getElementById('input').innerHTML=temp_input;		//put temporarily saved input into the textbox
	}
	else{
		document.getElementById('code_area').style.width='98%';
		temp_input=document.getElementById('input').innerHTML;		//save the current input to show it next time textbox is selected
		document.getElementById('input').style.display='none'
		document.getElementById('input').innerHTML='';				//clear the current data in textbox to put input to program = null
	}
}

if(document.getElementById("input").innerHTML)
	{
		document.getElementById("input").style.display='initial'
		document.getElementById("check_input").checked=true
		temp_input=document.getElementById('input').innerHTML;
		input_check();
	}

document.getElementById("check_input").addEventListener('change',input_check)

editor.on('change',updatetextarea);
function updatetextarea()
{
	document.getElementById('hiddentextarea').innerHTML=editor.getValue();
}

flag=lang_default		// gives the latest selected lang in drop down list
document.getElementById("lang").onchange=function(){
	lang=this.value 		//gives the currect selected lang in drop down list
	if(decode(document.getElementById('hiddentextarea').innerHTML)==source_template[flag])		//if code == template of last selected lang
		{
			flag=lang
			editor.setValue(source_template[lang])
		}
	lang=lang_map[lang]
	editor.getSession().setMode("ace/mode/"+lang)
};

//change the theme
document.getElementById("theme").onchange=function(){
	editor.setTheme('ace/theme/'+this.value);
};

//give the download option
document.getElementById("downloadCode").onclick=function(){      
// grab the content of the form field and place it into a variable
    var textToWrite = editor.getValue();
//  create a new Blob (html5 magic) that contains the data from your form feild
    var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});
// Specify the name of the file to be saved
	
	lang_extension={
		"C":".c",
		"C++":".cpp",
		"C++ 11":".cpp",
		"CLOJURE":".clj",
		"C#":".cs",
		"JAVA":".java",
		"JAVASCRIPT":".js",
		"HASKELL":".hs",
		"PERL":".pl",
		"PHP":".php",
		"PYTHON":".py",
		"RUBY":".rb"
	}

	var filename=prompt("Enter name of file to be saved : ")
	if(filename==null)
			return 

    var fileNameToSaveAs = filename+lang_extension[document.getElementById("lang").value];

// create a link for our script to 'click'
    var downloadLink = document.createElement("a");
//  supply the name of the file (from the var above).
// you could create the name here but using a var
// allows more flexability later.
    downloadLink.download = fileNameToSaveAs;
// provide text for the link. This will be hidden so you
// can actually use anything you want.
    downloadLink.innerHTML = "My Hidden Link";
    
// allow our code to work in webkit & Gecko based browsers
// without the need for a if / else block.
    window.URL = window.URL || window.webkitURL;
          
// Create the link Object.
    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
// when link is clicked call a function to remove it from
// the DOM in case user wants to save a second file.
    downloadLink.onclick = destroyClickedElement;
// make sure the link is hidden.
    downloadLink.style.display = "none";
// add the link to the DOM
    document.body.appendChild(downloadLink);
    
// click the new link
    downloadLink.click();
}

function destroyClickedElement(event)
{
// remove the link from the DOM
    document.body.removeChild(event.target);
}


document.getElementById("insertTemplate").onclick=function(){
	editor.setValue(source_template[document.getElementById("lang").value])
}


// EOF


/*document.getElementById('save').onclick=function(){
	localStorage.saved_code=document.getElementById('hiddentextarea').innerHTML
	window.alert("code saved successfully")
}

document.getElementById('retreive').onclick=function(){
	editor.setValue(decode(localStorage.saved_code))
}*/