# acr-extension-name

Arquivo config.json

```json
{
	"config": [
		{
			"kind": "enum",
			"message": "O enum `${NAME}` deve herdar de um dos tipos ${TYPEREF}.<br>Arquivo: ${PATH}.<br>Linha: ${LINE}",
			"typeref": [
				"typename:uint8_t",
				"typename:int8_t",
				"typename:uint16_t",
				"typename:int16_t",
				"typename:char"
			]
		}
	],
}
```
