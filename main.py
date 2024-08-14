import gradio as gr
import gr_tools

web_title = '知识库助手'
title_html = f'<h3 align="center">{web_title}</h3>'

with gr.Blocks(theme=gr.themes.Soft(), analytics_enabled=False) as demo:
    gr.HTML(title_html)
    with gr.Row():
        with gr.Column():
            upload_file = gr.File(label='本地资料库', file_count='multiple')
            chatbot = gr.Chatbot(height=700)
            # chatbot.style(height=580)

            with gr.Row():
                with gr.Column(scale=4):
                    input_text = gr.Textbox(show_label=False, placeholder="请输入你的问题")
                with gr.Column(scale=1, min_width=100):
                    submit_btn = gr.Button("提交", variant="primary")
                with gr.Column(scale=1, min_width=100):
                    clean_btn = gr.Button("清空", variant="stop")

    upload_file.upload(fn=gr_tools.get_file_content, inputs=[upload_file])
    input_text.submit(fn=gr_tools.chat, inputs=[input_text, chatbot], outputs=[chatbot], show_progress=True)
    input_text.submit(fn=lambda x: '', inputs=[input_text], outputs=[input_text], show_progress=True)
    #
    # submit_btn.click(fn=chat, inputs=[input_text, chatbot], outputs=[chatbot], show_progress=True)
    # submit_btn.click(fn=lambda x: '', inputs=[input_text], outputs=[input_text], show_progress=True)
    #
    # clean_btn.click(fn=lambda x: [], inputs=[chatbot], outputs=[chatbot])

demo.title = web_title
demo.queue().launch(share=False, server_name='0.0.0.0')