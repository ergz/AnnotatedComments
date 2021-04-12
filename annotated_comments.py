import sublime
import sublime_plugin

import re
import os

# TODO(emanuel) - it would be nice to be able to add custom "TODO" tags that the user
#                 may want to add to the list 


# TODO(emanuel) - need to improve this, I am not sure this is optimal
ANNOTATION_REGEX = {
    '.c': r"(//|/\*) ?(TODO|NOTE) ?\(.+\)?.+", 
    '.py': r"(#|\"\"\") ?(TODO|NOTE) ?\(.+\)?.+"
}



# TODO(emanuel) - find a way to exit nicely when there are no annotations or file not saved
def find_annotated_comments(view):

    if not view.file_name():
        sublime.message_dialog("File must be saved to detemine annotated comments!")
        return []
    else:
        regex_for_file = ANNOTATION_REGEX.get(os.path.splitext(view.file_name())[1])
        if not regex_for_file:
            sublime.status_message("This file contains no tags!")

        tags = [i for i in view.find_all(regex_for_file)]
        if not tags:
            sublime.message_dialog("This file contains no tags!")

        return tags

def parse_comment_annotation(s):
    result = re.search(r"(TODO|NOTE) ?\((.+)\) ?-? ?(.+)?", s)
    comment_desc = result.group(3) if result.group(3) else "no description provided!"
    return "{}({}): {}".format(result.group(1), result.group(2), comment_desc)

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


