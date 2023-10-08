# Distributing

* Increment version number in pyproject.toml
```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=mytoken 

python3 -m build

rm dist/*0.0.16*

pip3 uninstall sked_pitosalas

python3 -m twine upload --repository testpypi dist/* 
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps sked_pitosalas

pyenv rehash
```