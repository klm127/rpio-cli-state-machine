cd sphinx-doc
call make.bat html
cd ..
Xcopy /E /I .\sphinx-doc\build\html .\docs /y
rmdir /Q /S sphinx-doc\build
fsutil file createnew docs/.nojekyll 0