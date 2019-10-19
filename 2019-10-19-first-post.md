---
layout: page
title: "처음쓰는 POST입니다"
date: 2019-10-19 11:00:00 +0900
categories: jekyll update
---

# 제목 앞에는 #이 1개면 제목 타입
기본적인 문단은 그냥 작성하면 문단으로 인식

## 작아지는 제목

### 작아지는 제목2

[마크다운 문법확인하기][markdown-url] [markdown-url]: https://gist.github.com/ihoneymon/652be052a0727ad59601


<pre>

	#include <stdio.h>
	int stringEqual(const char *s1, const char *s2)
	{
	int i;

	for (i = 0; *(s1 + i) != '\0'; i++)
	{
		if (*(s2 + i) == '\0')
			return 1;
		if (*(s1 + i) != *(s2 + i))
			return 1;
	}
	if (*(s2 + i) != '\0')
		return 1;

	return 0;
	}
	void main()
	{
	char string1[50];
	char string2[50];

	printf("Enter the first string:");
	scanf("%s", string1);
	printf("Enter the second string:");
	scanf("%s", string2);

	if (stringEqual(string1, string2) == 0)
		printf("µÎ°³ÀÇ ¹®ÀÚ¿­Àº °°´Ù\n");
	else
		printf("µÎ°³ÀÇ ¹®ÀÚ¿­Àº ´Ù¸£´Ù\n");
	}

</pre>

test