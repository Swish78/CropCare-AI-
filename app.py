from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from collections import Counter
import tensorflow as tf
import os
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
CORS(app)

folder_path = "db"

cached_llm = Ollama(model="llama3")

embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=True
)

raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] You are a technical assistant skilled at searching documents for specific information. 
    If the provided documents do not contain an answer, clearly state that no relevant information was found. 
    Use the context to provide accurate and precise answers. [/INST] </s>
    [INST] 
    User Query: {input}
    Context from Documents: {context}
    Answer:
    [/INST]
    """
)

pdf_files = [
    "pdf/Disease2_Hort_Crops_20.04.2020.pdf",
]

models = {
    # 'banana': [tf.keras.models.load_model('Banana/model_resnet.h5'),
    #            tf.keras.models.load_model('Banana/model_lenet.h5'),
    #            tf.keras.models.load_model('Banana/model_inception.h5')],
    # 'wheat': [tf.keras.models.load_model('path/to/wheat_model1.h5'),
    #           tf.keras.models.load_model('path/to/wheat_model2.h5'),
    #           tf.keras.models.load_model('path/to/wheat_model3.h5')],
    # 'cotton': [tf.keras.models.load_model('path/to/cotton_model1.h5'),
    #            tf.keras.models.load_model('path/to/cotton_model2.h5'),
    #            tf.keras.models.load_model('path/to/cotton_model3.h5')],
    # 'watermelon': [tf.keras.models.load_model('path/to/watermelon_model1.h5'),
    #                tf.keras.models.load_model('path/to/watermelon_model2.h5'),
    #                tf.keras.models.load_model('path/to/watermelon_model3.h5')]
}


def process_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array


# def classify_image(crop, img_path):
#     img_array = process_image(img_path)
#     predictions = []
#
#     for model in models[crop]:
#         pred = model.predict(img_array)
#         pred_label = np.argmax(pred, axis=1)[0]
#         predictions.append(pred_label)
#
#     final_prediction = Counter(predictions).most_common(1)[0][0]
#     return final_prediction


# @app.route("/classify_crop", methods=["POST"])
# def classify_crop():
#     if 'file' not in request.files or 'crop' not in request.form:
#         return jsonify({'error': 'No file or crop type provided'}), 400
#
#     file = request.files['file']
#     crop = request.form['crop']
#
#     if crop not in models:
#         return jsonify({'error': 'Invalid crop type'}), 400
#
#     file_path = os.path.join('temp', file.filename)
#     file.save(file_path)
#
#     try:
#         prediction = classify_image(crop, file_path)
#         os.remove(file_path)
#         return jsonify({'prediction': prediction})
#     except Exception as e:
#         os.remove(file_path)
#         return jsonify({'error': str(e)}), 500


@app.route("/ai", methods=["POST"])
def aiPost():
    json_content = request.json
    query = json_content.get("query")
    response = cached_llm.invoke(query)
    response_answer = {"answer": response}
    return response_answer


@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    json_content = request.json
    query = json_content.get("query")

    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 50,
            "score_threshold": 0.1,
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    sources = []
    for doc in result["context"]:
        sources.append(
            {"source": doc.metadata["source"],
             "page_content": doc.page_content
             }
        )

    response_answer = {"answer": result["answer"], "sources": sources}
    return response_answer


@app.route("/pdf", methods=["POST"])
def pdfPost():
    for pdf_file in pdf_files:
        loader = PDFPlumberLoader(pdf_file)
        docs = loader.load_and_split()
        chunks = text_splitter.split_documents(docs)
        vector_store = Chroma.from_documents(
            documents=chunks, embedding=embedding, persist_directory=folder_path
        )
        vector_store.persist()

        response = {
            "status": "Successfully Processed",
            "filename": pdf_file,
            "doc_len": len(docs),
            "chunks": len(chunks),
        }

    return response


def start_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    start_app()