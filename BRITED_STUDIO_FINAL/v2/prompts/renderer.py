import re


class PromptRenderer:
    """
    Renderer simple de variables de prompt.

    Supporte les syntaxes :

    {{variable}}
    {{ variable }}
    {{  variable  }}

    Une erreur est levée lorsqu'une variable
    non résolue subsiste dans le prompt final.
    """

    VARIABLE_PATTERN = re.compile(
        r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}"
    )

    @classmethod
    def render(
        cls,
        prompt: str,
        **variables,
    ) -> str:
        """
        Remplace les variables présentes dans le prompt.
        """

        def replace_variable(
            match: re.Match,
        ) -> str:

            key = match.group(1)

            if key not in variables:

                raise ValueError(
                    "Variable de prompt non fournie : "
                    f"{key}"
                )

            value = variables[key]

            if value is None:
                return ""

            return str(value)

        rendered_prompt = cls.VARIABLE_PATTERN.sub(
            replace_variable,
            prompt,
        )

        unresolved_variables = (
            cls.VARIABLE_PATTERN.findall(
                rendered_prompt
            )
        )

        if unresolved_variables:

            raise ValueError(
                "Variables de prompt non résolues : "
                + ", ".join(
                    sorted(
                        set(unresolved_variables)
                    )
                )
            )

        return rendered_prompt
    