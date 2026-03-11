
 CEVM_CultureEventVendingMachine
### Group Project for 'Text Understanding and AI'

This repository implements a **Retrieval-Augmented Generation (RAG)** system integrated with a **Fine-tuned Llama-3-8B** model, specifically optimized for personalized cultural event discovery in Seoul. By leveraging **Parameter-Efficient Fine-Tuning (PEFT)** techniques, the system provides context-aware recommendations tailored to diverse user personas.

<img width="633" height="307" alt="화면 캡처 2026-03-11 000146" src="https://github.com/user-attachments/assets/d9b1885c-200d-4c18-a2df-7c288443a776" />

---

## System Overview
The project aims to solve the fragmentation of cultural information by providing a unified, persona-sensitive recommendation engine. It combines the factual grounding of **RAG** with the stylistic flexibility of a fine-tuned **Large Language Model (LLM)** to deliver accurate and tone-appropriate responses.

---

## Technical Specifications

### Core Technologies
* **Base Model**: `beomi/Llama-3-Open-Ko-8B`
* **Fine-tuning Technique**: QLoRA (4-bit Quantization)
* **PEFT Library**: Hugging Face PEFT (LoRA)
* **Training Environment**: Google Colab (Tesla T4 GPU)
* **Data Pipeline**: Python, Pandas, JSON-based ETL

### Fine-tuning Configuration
* **Rank (r)**: 32
* **Alpha**: 16
* **Target Modules**: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
* **Optimization**: BitsAndBytes 4-bit quantization for memory efficiency

---

## Methodology

### 1. Dataset Engineering
* **Knowledge Source**: 4,275 official cultural event records from the Seoul Open Data Plaza.
* **Instruction Tuning**: Developed 130 high-quality instruction-input-output triplets to define model behavior.
* **Persona Mapping**: Integrated specific user profiles (e.g., budget-sensitive students, families, seniors) into the training data to modulate response tone and filtering logic.

### 2. RAG Pipeline Implementation
* **Retriever**: Implemented a metadata-based search module to extract relevant event context including Title, Place, Price, and Category.
* **Prompt Engineering**: Designed a Chat Template that injects retrieved context and persona information into the LLM's input to ensure factual consistency and stylistic alignment.

### 3. Training Process
* **SFT**: Utilized `SFTTrainer` for supervised fine-tuning.
* **Convergence**: Monitored training loss convergence, achieving a reduction from an initial 1.8 to a final **0.7**.
* **Hyperparameter Sweeps**: Performed sweeps across various LoRA ranks (8, 16, 32, 64) to find the optimal balance between computational overhead and model representational power.

---

## Problem Solving and Optimization

* **Data Integrity**: Resolved complex encoding issues (UTF-8/CP949) found in public CSV files by migrating the entire pipeline to a JSON-based structure, ensuring zero information loss.
* **VRAM Management**: Mitigated GPU memory leaks during evaluation and inference loops by implementing manual session restarts and runtime cache clearing.
* **Model Selection**: Evaluated multiple architectures including Polyglot-0.5B and Qwen-2.5-7B, ultimately selecting **Llama-3-8B** for its superior Grouped-Query Attention (GQA) benefits and multi-turn instruction-following performance.

---

## Quantitative Metrics

### 1. Training Loss Convergence
* **Loss Reduction**: The training loss successfully converged from an initial 1.8 to the 0.7 range during the fine-tuning process.
* **Optimization Path**: Monitored through a step-by-step training process, the loss showed a consistent downward trend, reaching as low as 0.30 at the final steps.

### 2. ROUGE-L Benchmarking
* **Knowledge Retrieval (High Precision)**: The model achieved a ROUGE-L score of 0.83 on tasks requiring specific information extraction from the retrieved context.
* **Generative Flexibility**: For general conversational responses, the score was recorded at 0.046, indicating the model's ability to generate natural, varied dialogue rather than verbatim copying.

### 3. Hyperparameter Optimization (LoRA Rank)
* **Rank Analysis**: Experimental sweeps were conducted across ranks 8, 16, and 32 to identify the optimal balance between computational overhead and performance.
* **The "Sweet Spot"**: Rank 32 was identified as the optimal configuration, providing the lowest final loss (1.51) compared to Rank 8 (2.15) and Rank 16 (1.79) within the tested environment.

---

## Qualitative Assessment

### 1. Advanced Information Filtering
* **Constraint Satisfaction**: The model successfully filtered event data based on complex queries, such as identifying performances under a specific price threshold (e.g., "under 15,000 KRW").
* **Factual Grounding**: By utilizing the RAG pipeline, the model significantly reduced hallucinations by grounding its recommendations in verified public records.

### 2. Comparative Reasoning
* **Nuance Detection**: The system demonstrated the ability to explain qualitative differences between retrieved items, such as describing the varying levels of intensity between "15+ rated" and "12+ rated" performances.

### 3. Multi-Persona Adaptation
* **Tone and Manner**: Validation confirmed the model's ability to switch communication styles based on the user's profile, such as providing budget-focused advice for students and honorific-rich responses for senior citizens.

---

## Technical Constraints & Limitations

### 1. Quantization Trade-offs
* **4-bit Compression**: To fit within the VRAM limits of the Google Colab T4 environment, 4-bit quantization (QLoRA) was utilized.
* **Impact**: While highly efficient, this compression may lead to slight degradations in the model's ability to capture extremely fine linguistic nuances compared to the uncompressed base model.

### 2. Evaluation Scope
* **Metric Subjectivity**: Standard metrics like ROUGE may not fully capture the context or "naturalness" of a persona-based response, suggesting a need for advanced LLM-based automated evaluation in future iterations.

---

## Model Metadata
* **Base Model**: beomi/Llama-3-Open-Ko-8B
* **Adapter**: hushpond/llama-3-seoul-culture-lora-rag
* **Framework**: PEFT / LoRA / QLoRA

## Model Access
The fine-tuned LoRA adapter is hosted on Hugging Face:
[hushpond/llama-3-seoul-culture-lora-rag](https://huggingface.co/hushpond/llama-3-seoul-culture-lora-rag)

---

## Future Development
* Implementation of 8-bit quantization for higher inference precision.
* Integration of Reinforcement Learning from Human Feedback (RLHF) to further refine recommendation nuances.
* Development of a React-based front-end for real-time mobile accessibility.

---

## Data Sources
* [KOPIS Open API](https://kopis.or.kr/por/cs/openapi/openApiList.do?menuId=MNU_00074&tabId=tab1_1)
* [Training Dataset (Google Sheets)](https://docs.google.com/spreadsheets/d/1xIgswlovpABGyzf0uKfSIBD9_TKWo2o_I3GVx2mHtI4/edit?usp=sharing)
