# AnnotatedComments

A sublime text (3+) plugin that will allow you navigate through annotated comments.

*What is an annotated comment?*

For now an annotated comment is a comment that starts with one of *TODO* or *NOTE* followed
by a user name and optionally followed by a description. In code this looks like this:

```c
// TODO(ergz) - make this work with more languages
/* TODO(ergz) - it currently has too many things baked in */
```

It's probably a good idea when annotating comments that you add a short description 
along with the TODO, if you need more than what would fit the quick_panel please add 
this in a new line.