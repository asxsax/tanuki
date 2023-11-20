from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')
prompt = "This is a"
generated_text = generator(prompt, max_length=8, num_return_sequences=1)

print(generated_text[0]['generated_text'])
