cd sphinx-doc
call make.bat html
cd ..
Xcopy /E /I .\sphinx-doc\build\html .\docs /y