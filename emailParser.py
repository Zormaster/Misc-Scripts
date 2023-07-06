from email_reply_parser import EmailReplyParser
import re

# Define HMTL cleaning function
def clean_comment(comment):
    comment = EmailReplyParser.parse_reply(comment)

    # block = re.compile(r'`{3,}.*?`{3,}|<pre>.*?</pre>|^(?: {4,}|\t+).*?$', re.MULTILINE | re.DOTALL)
    # comment = block.sub('', comment)

    # inline = re.compile(r'`.*?`', re.MULTILINE | re.DOTALL)
    # comment = inline.sub('', comment)

    # link = re.compile(r'!?\[(.*?)\]\(.*?\)', re.MULTILINE | re.DOTALL)
    # comment = link.sub(r'\1', comment)

    # url = re.compile(r'\(?https?://\S+\)?', re.MULTILINE | re.DOTALL)
    # comment = url.sub('', comment)

    # code = re.compile(r'(?:[A-Z][a-z]*){2,}(?:::(?:[A-Z][a-z]*)+)*(?:\.|#\S+)*', re.MULTILINE | re.DOTALL)
    # comment = code.sub('', comment)

    # ruby = re.compile(r'(?:\w+/)*\w*\.rb', re.MULTILINE | re.DOTALL)
    # comment = ruby.sub('', comment)

    emoji = re.compile(r':\S+:', re.MULTILINE | re.DOTALL)
    comment = emoji.sub('', comment)

    tag = re.compile(r'(\<[^a].*?\>)', re.MULTILINE | re.DOTALL)
    comment = tag.sub('', comment)

    snc = re.compile(r'#snc_notification.*? \{.*?\}', re.MULTILINE | re.DOTALL)
    comment = snc.sub('', comment)

    return comment


msg = '''<!DOCTYPE html>
<html>
<head>
    <title>Email Example</title>
</head>
<body>
    <h1>Example Email</h1>
    
    <p>Dear recipient,</p>
    
    <p>I wanted to share some important information with you:</p>
    
    <ul>
        <li>An IP address: <code>192.168.0.1</code></li>
        <li>An email address: <a href="mailto:example@example.com">example@example.com</a></li>
        <li>A website link: <a href="https://www.example.com">www.example.com</a></li>
    </ul>
    
    <p>Please let me know if you have any questions or need further assistance.</p>
    
    <p>Best regards,</p>
    <p>Example Name</p>
    
</body>
</html>
'''
print(clean_comment(msg))
