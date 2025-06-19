Ok Geep, let's set some ground rules here.

Rules listed in order of priority:
- We want the codebase to be kawaii. 
  - Unless that sacrifices practicality to some large extent.
- Our tabs are 2 spaces here, not 4. Edgy, I know, but that's how we roll here.
- Try to avoid advanced overengineering stuff that's hard to read, like decorators, functional stuff, huuge chains of builders and factories and whatever, all kinds of tricky python shorthand like complex inlining. Rather just like stick to the basics your grandma could read.
  - Though object oriented stuff is fair game.
- Docstrings should be written in the sphinx style.
  - Though don't go out of your way to reformat old code if you see functions that don't use the sphinx style.
  - Also geep if you write some code, feel free to add an extra short .. note: block with instructions that let you specifically understand the code better. I mean I get how you might prefer some format that wouldn't necessarily be a human's cup of tea. Everyone got their own thing, I get it.
- We wanna minimize the bloating of requirments.txt
- Ye in this codebase we don't use type hints. If there's something nonobvious about the types, rather just describe that in the docstring.