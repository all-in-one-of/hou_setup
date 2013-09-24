unix echo "456"
exread $HOME/houdini12.0/scripts/custom_expressions.expr
setenv HIPBASE=`substr($HIPNAME,0,rindex($HIPNAME,"_"))`
setenv HIPBASENAME=`substr($HIPNAME,0,rindex($HIPNAME,"."))`
setenv VER=`substr($HIPBASENAME,rindex($HIPBASENAME,"_")+2,strlen($HIPBASENAME)-rindex($HIPBASENAME,"_")+2)`
