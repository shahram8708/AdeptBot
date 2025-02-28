import torch
import base64
import urllib.request
from io import BytesIO
from PIL import Image
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
from pdf2image import convert_from_path

def render_pdf_to_base64png(pdf_path, page_number, target_longest_image_dim=1024):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    img = images[0]
    img.thumbnail((target_longest_image_dim, target_longest_image_dim))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

model = Qwen2VLForConditionalGeneration.from_pretrained("allenai/olmOCR-7B-0225-preview", torch_dtype=torch.bfloat16).eval()
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

pdf_url = "https://molmo.allenai.org/paper.pdf"
pdf_path = "./paper.pdf"
urllib.request.urlretrieve(pdf_url, pdf_path)

image_base64 = render_pdf_to_base64png(pdf_path, 1, target_longest_image_dim=1024)

prompt = "Extract and summarize key information from the document."

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
        ],
    }
]

text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
main_image = Image.open(BytesIO(base64.b64decode(image_base64)))

inputs = processor(
    text=[text],
    images=[main_image],
    padding=True,
    return_tensors="pt",
)
inputs = {key: value.to(device) for (key, value) in inputs.items()}

output = model.generate(
    **inputs,
    temperature=0.8,
    max_new_tokens=50,
    num_return_sequences=1,
    do_sample=True,
)

prompt_length = inputs["input_ids"].shape[1]
new_tokens = output[:, prompt_length:]
text_output = processor.tokenizer.batch_decode(new_tokens, skip_special_tokens=True)

print(text_output)
