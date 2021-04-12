import sublime
import sublime_plugin

import re
import os

# TODO(bug) - status message shows when keybinding is pressed at quickpanel is open
# it would be nice if instead it just closed itself sorta like what ctrl+P does


# TODO(feature) - add additional comment annotations
# other potential annotations could be: SECTION, 


# TODO(optimize)
ANNOTATION_REGEX = {
    '.c': r"(//|/\*) ?(TODO|NOTE|SECTION) ?\(.+\)?.+", 
    '.py': r"(#) ?(TODO|NOTE|SECTION) ?\(.+\)?.+"
}


# TODO(refactor) - find a way to exit nicely when there are no annotations or file not saved
# I am not very good at python, and so would like exit this program ASAP when it makes sense to
def find_annotated_comments(view):

    if not view.file_name():
        sublime.message_dialog("File must be saved to detemine annotated comments!")
        return []
    else:
        regex_for_file = ANNOTATION_REGEX.get(os.path.splitext(view.file_name())[1])
        if not regex_for_file:
            sublime.status_message("This file contains no tags!")

        tags = [i for i in view.find_all(regex_for_file, sublime.IGNORECASE)]
        if not tags:
            sublime.message_dialog("This file contains no tags!")

        return tags

def parse_comment_annotation(s):
    result = re.search(r"(TODO|NOTE|SECTION) ?\((.+)\) ?(-|:)? ?(.+)?", s)

    if result.group(1) == "SECTION":
        comment_desc = "-----------"
    else:
        comment_desc = result.group(4) if result.group(4) else "no description provided!"
    return "{}({}): {}".format(result.group(1), result.group(2), comment_desc)
    # return ["{}({})".format(result.group(1), result.group(2)), "{}".format(comment_desc)]

class AnnotatedCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit, start=None, end=None):
        if start is None:
            return self.prompt_tag()
        
        selected_region = sublime.Region(start, end)
        try:
            self.view.sel().clear()
            self.view.sel().add(selected_region)
            self.view.show(selected_region)

        except ValueError:
            sublime.status_message("'%s' not found in this file" % self.view.substr(tag))

    def prompt_tag(self):
        items = find_annotated_comments(self.view)
        display_items = [parse_comment_annotation(self.view.substr(j)) for j in items]
        def pick(idx):
            if idx != -1:
                region_of_selected = items[idx]
                self.view.run_command("annotated_comments", {"start": region_of_selected.begin(), 
                                                            "end": region_of_selected.end()})

        self.view.window().show_quick_panel(
            display_items,
            lambda idx: pick(idx),
            sublime.MONOSPACE_FONT,
            0, 
            lambda idx: pick(idx))
