# В этой папке будут собраны другие лаборатоные, которые буду теститься на данном проекте

## lab_5 (Impove_It)
[Описание тулзов](https://proglib.io/p/python-code-analysis)

### Pycodestyle
![image](https://user-images.githubusercontent.com/78679833/150684391-377ecda1-4527-490d-b2e8-f59cee84b4a5.png)

Убрал все длинные строки.

Как переписать голый except не придумал

![image](https://user-images.githubusercontent.com/78679833/150684968-7add7b6a-e9aa-4207-a1e2-87fd1212b23f.png)

### pyflakes
![image](https://user-images.githubusercontent.com/78679833/150685309-f6b116b1-3d45-46ae-939a-ebc7d6754b57.png)

Оказалось что у меня все испорты используются, но для примера я дописал import os что бы проверить что pyflakes работаети и он его вывел как не используемый import. Я его удалил.

### mypy

Решил потестить на клиенте
![image](https://user-images.githubusercontent.com/78679833/150685629-f4e5746f-8f7b-4af6-8da8-eeda2097cfdd.png)

Прописал pip install types-requests и он перестал выдавать ошибки

![image](https://user-images.githubusercontent.com/78679833/150685682-a65b0992-b724-4a87-9342-14a75e40db17.png)

