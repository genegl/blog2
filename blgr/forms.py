from django import forms
from blgr.models import Post, Comments

class PostForm(forms.ModelForm):

	class Meta():
		model = Post
		fields = ('author', 'title', 'text')

		widgets = {		# this is design of the post form (title and text) 
			'title':forms.TextInput(attrs={'class':'textinputclass'}),	# css class textinputclass
			'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})	# css class editable
		}



class CommentForm(forms.ModelForm):

	class Meta():
		model = Comment
		fields = ('author', 'text')

		widgets = {
			'author':forms.TextInput(attrs={'class':'textinputclass'}),
			'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
		}