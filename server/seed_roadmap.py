"""Seed the ML Roadmap into the learning assistant as regular Item objects."""

from __future__ import annotations

from models import Item, ItemState, ItemType
from services.sqlite_repo import list_items, save_item

USER_ID = "demo-user"

_CERTIFICATIONS = [
    {
        "name": "Google Professional ML Engineer",
        "provider": "Google Cloud",
        "effort": "~40 hrs prep",
        "duration": "Weeks 8–10",
        "salary": "+12–18% leverage in negotiation",
        "tag": "HIGHEST ROI",
        "desc": "The gold standard for ML at Google. Tests distributed training, model deployment, MLOps, Vertex AI, and bias/fairness — topics you'll have mastered by week 8.",
        "url": "https://cloud.google.com/certification/machine-learning-engineer",
    },
    {
        "name": "Deep Learning Specialization",
        "provider": "deeplearning.ai / Coursera",
        "effort": "~60 hrs",
        "duration": "Weeks 1–4 (parallel)",
        "salary": "Industry baseline credential",
        "tag": "ESSENTIAL",
        "desc": "Andrew Ng's 5-course series. Do it in parallel with Phase 1 — it reinforces your math with practical framing. The certificate is widely recognized.",
        "url": "https://deeplearning.ai/courses/deep-learning-specialization",
    },
    {
        "name": "MLOps Specialization",
        "provider": "deeplearning.ai / Coursera",
        "effort": "~30 hrs",
        "duration": "Weeks 9–11 (parallel)",
        "salary": "Critical for senior roles",
        "tag": "SENIOR SIGNAL",
        "desc": "Bridges research and production. Covers data pipelines, model monitoring, CI/CD for ML, feature stores — exactly what senior engineers are grilled on.",
        "url": "https://deeplearning.ai/courses/machine-learning-engineering-for-production-mlops",
    },
    {
        "name": "AWS ML Specialty",
        "provider": "Amazon Web Services",
        "effort": "~25 hrs prep",
        "duration": "Weeks 11–12",
        "salary": "+10–15% in AWS-heavy orgs",
        "tag": "MULTI-CLOUD",
        "desc": "Broadens your cloud credibility beyond GCP. Useful if targeting non-Google FAANG or startups. SageMaker, Rekognition, MLOps on AWS.",
        "url": "https://aws.amazon.com/certification/certified-machine-learning-specialty",
    },
    {
        "name": "Kaggle Competitions Master/Grandmaster",
        "provider": "Kaggle",
        "effort": "~80 hrs across 3 months",
        "duration": "Ongoing — start Week 2",
        "salary": "Direct proof of skill — often beats certs",
        "tag": "PROOF OF SKILL",
        "desc": "Top 50 finish in any featured competition is worth more than any certificate. Start with tabular competitions, progress to CV/NLP.",
        "url": "https://kaggle.com/competitions",
    },
    {
        "name": "TensorFlow Developer Certificate",
        "provider": "Google / TensorFlow",
        "effort": "~10 hrs prep",
        "duration": "Week 6",
        "salary": "Entry signal, less critical at senior level",
        "tag": "FOUNDATIONAL",
        "desc": "Quick win if you're fast with Keras/TF. Worth doing in a weekend — verifies practical implementation speed to Google-affiliated roles.",
        "url": "https://tensorflow.org/certificate",
    },
    {
        "name": "Hugging Face NLP / Transformers Course",
        "provider": "Hugging Face",
        "effort": "~20 hrs",
        "duration": "Weeks 5–6 (parallel)",
        "salary": "Community credibility + industry recognition",
        "tag": "FREE + HIGH SIGNAL",
        "desc": "Free, but the completion badge and community presence matter. Shows practical LLM ecosystem fluency — the HF hub is where the industry lives.",
        "url": "https://huggingface.co/learn",
    },
    {
        "name": "Stanford CS229 / CS231n (Audit)",
        "provider": "Stanford Online",
        "effort": "~50 hrs selected lectures",
        "duration": "Weeks 1–8 (background reading)",
        "salary": "Research credibility — cited in interviews",
        "tag": "RESEARCH SIGNAL",
        "desc": "Not a certificate but frequently cited by researchers. Select problem sets strengthen theoretical foundations. Do problem sets even when auditing.",
        "url": "https://cs229.stanford.edu",
    },
]

_PHASES = [
    {
        "label": "Phase 1",
        "weeks": "Weeks 1–4",
        "title": "Mathematical & Algorithmic Arsenal",
        "weekly_hours": 100,
        "tagline": "If you don't own the math, you rent the intuition.",
        "milestone": "Implement every classic ML algorithm from scratch. Pass CS229 problem sets cold.",
        "goals": [
            "Derive and implement backpropagation from scratch without frameworks",
            "Implement gradient descent, Adam, L-BFGS with convergence proofs",
            "Understand every Bishop chapter without skipping proofs",
            "Complete Deep Learning Specialization (Coursera) in parallel",
            "First Kaggle competition submission — top 40%",
        ],
        "domains": [
            {
                "name": "Linear Algebra — ML Depth",
                "priority": "CRITICAL",
                "topics": [
                    "SVD: thin/full, economy, pseudoinverse — implement PCA, LSA, and low-rank approximation from scratch",
                    "Eigendecomposition: spectral theorem, PSD matrices, quadratic forms, Rayleigh quotient",
                    "Matrix calculus: Jacobians, Hessians, chain rule in matrix form — denominator vs numerator layout conventions",
                    "Woodbury identity & matrix inversion lemma — apply to GP posterior, ridge regression, kernel methods",
                    "Kronecker products: appear in multi-task learning, tensor factorizations, Kronecker-factored curvature (K-FAC)",
                    "Cholesky decomposition: numerical stability in GP inference and linear systems",
                    "Tensor algebra: CP decomposition, Tucker, tensor train — representations behind deep learning parameter sharing",
                    "Random matrix theory: Marchenko-Pastur law, bulk eigenvalue distribution — explains why overparameterized networks generalize",
                ],
            },
            {
                "name": "Probability & Bayesian Inference",
                "priority": "CRITICAL",
                "topics": [
                    "Exponential family: canonical form, sufficient statistics, log-partition function A(η), conjugacy",
                    "Bayesian model comparison: marginal likelihood, Bayes factor, Occam's razor geometric interpretation",
                    "KL divergence: asymmetry, forward (mean-seeking) vs reverse (mode-seeking) KL, f-divergences",
                    "Variational Inference: ELBO derivation, mean-field factorization, CAVI algorithm — implement for GMM",
                    "EM Algorithm: complete-data log-likelihood, Jensen's inequality proof, M-step optimality guarantees",
                    "Gaussian Processes: kernel = covariance function, GP regression posterior, marginal likelihood optimization",
                    "Markov Chain Monte Carlo: Metropolis-Hastings, Gibbs sampling, Hamiltonian MC (HMC) with momentum",
                    "Sequential Monte Carlo: particle filters, importance resampling — apply to state-space models",
                ],
            },
            {
                "name": "Optimization Theory — Deep",
                "priority": "CRITICAL",
                "topics": [
                    "Convex analysis: convex sets, functions, epigraphs, sublevel sets, conjugate functions",
                    "First & second-order optimality: KKT conditions, strong duality, constraint qualification",
                    "Gradient descent convergence: Lipschitz smoothness (L), strong convexity (μ), condition number κ=L/μ",
                    "Momentum methods: Polyak heavy ball, Nesterov acceleration — O(1/k²) vs O(1/k) convergence",
                    "Newton's method: quadratic convergence, Hessian cost, trust region modifications",
                    "Conjugate gradient: Lanczos connection, efficient large-scale linear systems",
                    "Stochastic optimization: SGD variance, mini-batch variance, importance sampling for variance reduction",
                    "Non-convex landscapes: saddle points, strict saddle property, global optima in overparameterized nets",
                ],
            },
            {
                "name": "Information Theory",
                "priority": "HIGH",
                "topics": [
                    "Entropy, cross-entropy, conditional entropy: chain rules, data processing inequality",
                    "Mutual information: relationship to KL, sufficient statistics, InfoMax principle",
                    "Rate-distortion theory: lossy compression, β-VAE connection to information bottleneck",
                    "Minimum description length (MDL): connections to Bayesian model selection",
                    "Maximum entropy principle: derive Gaussian from mean/variance constraints, Boltzmann distribution",
                    "Information geometry: Fisher metric, natural gradient as steepest descent in distribution space",
                ],
            },
            {
                "name": "Classical ML — Expert Level",
                "priority": "HIGH",
                "topics": [
                    "SVMs: primal/dual, kernel trick derivation, soft-margin, SMO algorithm — implement from scratch",
                    "Decision Trees: impurity measures (Gini, entropy), CART algorithm, tree depth vs bias-variance",
                    "Ensemble methods: Bagging (variance reduction proof), Random Forests (decorrelation), Gradient Boosting",
                    "XGBoost internals: second-order Taylor expansion, regularization tree complexity, weighted quantile sketch",
                    "Dimensionality reduction: PCA, ICA, UMAP (graph Laplacian, fuzzy topology), t-SNE",
                    "Clustering: k-means, GMM-EM, spectral clustering (normalized Laplacian), DBSCAN",
                    "Causal inference: do-calculus, backdoor criterion, instrumental variables",
                ],
            },
        ],
    },
    {
        "label": "Phase 2",
        "weeks": "Weeks 5–8",
        "title": "Deep Learning — Total Mastery",
        "weekly_hours": 160,
        "tagline": "Know every architecture well enough to improve it.",
        "milestone": "Implement Transformer, Diffusion Model, and VAE from scratch in both PyTorch and JAX. Fine-tune an LLM.",
        "goals": [
            "Implement multi-head attention, positional encodings, LayerNorm from scratch in PyTorch AND JAX",
            "Train a GPT-2 scale model on custom data from scratch",
            "Fine-tune Llama/Mistral with LoRA and DPO",
            "Implement DDPM diffusion model from scratch",
            "Complete Hugging Face Transformers course + earn TF Developer cert",
            "Kaggle: top 20% in an NLP or CV featured competition",
        ],
        "domains": [
            {
                "name": "Backprop & Autodiff — Internals",
                "priority": "CRITICAL",
                "topics": [
                    "Automatic differentiation: forward vs reverse mode, why reverse is O(n) for n parameters vs O(n²) forward",
                    "Computation graph: static (TF1) vs dynamic (PyTorch eager), tape-based AD, jaxpr tracing in JAX",
                    "Implement a toy autograd engine (Micrograd-level) — understand every operator's backward pass",
                    "Vanishing/exploding gradients: gradient norm tracking, Jacobian singular values, skip connections as fix",
                    "Mixed precision training: FP16 loss scaling, BF16 stability, TF32 on Ampere GPUs",
                    "Gradient checkpointing: trade FLOPs for memory — critical for long-sequence training",
                ],
            },
            {
                "name": "Transformers — Complete",
                "priority": "CRITICAL",
                "topics": [
                    "Self-attention mechanics: Q/K/V projections, scaled dot-product, why scale by √d_k",
                    "Multi-head attention: subspace diversity, implementation via reshape not separate projections",
                    "Positional encodings: sinusoidal, learned, RoPE (rotation matrix intuition), ALiBi, YaRN",
                    "Layer normalization: Pre-LN vs Post-LN stability, RMSNorm, why it matters",
                    "Flash Attention v1/v2/v3: IO-aware tiling, why HBM bandwidth is the bottleneck not FLOPs",
                    "KV caching: inference optimization, GQA (grouped query attention), MQA, memory math",
                    "Mixture of Experts: top-k routing, load balancing auxiliary loss, capacity factor",
                    "Implement GPT-2 from scratch: tokenization, data pipeline, training loop, evaluation",
                ],
            },
            {
                "name": "Large Language Models — Full Stack",
                "priority": "CRITICAL",
                "topics": [
                    "Pretraining: causal LM objective, data curation, deduplication (MinHash, SimHash)",
                    "Scaling laws: Kaplan (2020) vs Chinchilla (2022) — compute-optimal training, IsoFLOP curves",
                    "RLHF: reward model training (Bradley-Terry), PPO for LMs, KL penalty, reward hacking",
                    "DPO: direct preference optimization — bypass reward model, implicit reward derivation",
                    "Fine-tuning: full fine-tune, LoRA (rank decomposition), QLoRA (4-bit NF4), adapter layers",
                    "RAG: dense retrieval (DPR), chunking strategies, reranking (cross-encoder), FLARE, Self-RAG",
                    "Inference: speculative decoding, continuous batching, PagedAttention (vLLM), beam search",
                    "Multimodal LLMs: CLIP alignment, visual tokens, LLaVA, Flamingo, GPT-4V architecture principles",
                ],
            },
            {
                "name": "Generative Models",
                "priority": "CRITICAL",
                "topics": [
                    "VAEs: ELBO derivation, reparameterization trick, posterior collapse, β-VAE, VQ-VAE",
                    "GANs: minimax game, JS divergence, Wasserstein GAN (Kantorovich duality), spectral normalization",
                    "Diffusion Models: forward process (q), reverse process (p), DDPM score matching connection",
                    "DDIM: non-Markovian sampling, deterministic inversion, 10× fewer steps",
                    "Flow Matching: straight-line ODE paths, superior to diffusion in training efficiency",
                    "Consistency Models: single-step generation, distillation from diffusion",
                ],
            },
            {
                "name": "Representation Learning & Self-Supervised",
                "priority": "HIGH",
                "topics": [
                    "Contrastive learning: InfoNCE loss (mutual information lower bound), temperature scaling",
                    "SimCLR: augmentation strategy, projection head, why large batch matters",
                    "MoCo: momentum encoder, memory queue — decouples batch size from negatives",
                    "BYOL / SimSiam: no negatives — stop gradient prevents collapse",
                    "DINO / DINOv2: self-distillation with no labels, patch-based features, emergent segmentation",
                    "Masked Autoencoders (MAE): 75% masking ratio, asymmetric encoder-decoder, patch reconstruction",
                ],
            },
            {
                "name": "Reinforcement Learning",
                "priority": "HIGH",
                "topics": [
                    "MDP fundamentals: Bellman equations, value/policy iteration — prove convergence",
                    "Policy gradient: REINFORCE, baseline subtraction (variance reduction), actor-critic",
                    "PPO: clipped surrogate objective, value function clipping, why it's stable",
                    "Q-learning: DQN, double DQN, dueling networks, prioritized replay",
                    "Model-based RL: Dreamer (latent dynamics, RSSM), world models, imagination rollouts",
                    "RL for LLMs: PPO in RLHF, token-level vs sequence-level rewards",
                ],
            },
        ],
    },
    {
        "label": "Phase 3",
        "weeks": "Weeks 9–11",
        "title": "Systems, Scale & Production",
        "weekly_hours": 132,
        "tagline": "Research without systems thinking doesn't ship. Systems without research doesn't innovate.",
        "milestone": "Train a model on 4+ GPUs with custom distributed strategy. Design a complete ML system end-to-end.",
        "goals": [
            "Implement data parallel + tensor parallel training from scratch in JAX (pmap + sharding)",
            "Deploy a fine-tuned LLM with vLLM, measure latency/throughput tradeoffs",
            "Pass Google Professional ML Engineer exam",
            "Complete MLOps Specialization (deeplearning.ai)",
            "Build one production-grade ML project: full pipeline from data → training → serving → monitoring",
        ],
        "domains": [
            {
                "name": "JAX — Expert Level",
                "priority": "CRITICAL",
                "topics": [
                    "Functional programming paradigm: pure functions, immutable state, why JAX demands this",
                    "jit compilation: tracing vs interpretation, static vs dynamic shapes, pytree structures",
                    "grad / value_and_grad / jvp / vjp: custom Jacobian-vector products, higher-order derivatives",
                    "vmap: vectorization over arbitrary batch dimensions, nested vmap, vmap + grad combinations",
                    "pmap: SPMD parallelism, device mesh, pmean/psum/pmax for collective operations",
                    "Sharding API: jax.sharding.NamedSharding, GSPMDSharding, Mesh",
                    "XLA compilation: HLO IR, op fusion, why XLA outperforms PyTorch on TPUs",
                    "Flax/Linen: module system, parameter trees, variable collections",
                    "Implement Transformer, CNN, LSTM from scratch in JAX — no Flax, just lax and numpy",
                ],
            },
            {
                "name": "Distributed Training",
                "priority": "CRITICAL",
                "topics": [
                    "Data parallelism: allreduce, ring allreduce, gradient accumulation — implement with pmap in JAX",
                    "Tensor parallelism: column/row partition of weight matrices, Megatron-LM style",
                    "Pipeline parallelism: stage assignment, micro-batching, GPipe schedule, 1F1B schedule",
                    "FSDP: parameter sharding, forward gather, backward scatter, mixed with TP",
                    "3D parallelism: data × tensor × pipeline — how Megatron-Turing NLG, PaLM were trained",
                    "ZeRO optimizer stages 1/2/3: memory vs communication tradeoffs",
                    "Communication primitives: broadcast, scatter, gather, allreduce, reduce-scatter",
                ],
            },
            {
                "name": "Inference Optimization",
                "priority": "CRITICAL",
                "topics": [
                    "Quantization: post-training quantization (PTQ), QAT, INT8/INT4, GPTQ, AWQ, SmoothQuant",
                    "Knowledge distillation: temperature scaling, soft labels, intermediate layer distillation",
                    "Pruning: structured vs unstructured, magnitude pruning, lottery ticket hypothesis",
                    "Speculative decoding: draft model + verifier, γ acceptance rate, theoretical speedup analysis",
                    "Continuous batching: dynamic batching for variable-length LLM sequences (vLLM, TGI)",
                    "PagedAttention: KV cache memory management, block tables",
                    "TensorRT: graph optimization, layer fusion, calibration for INT8",
                ],
            },
            {
                "name": "MLOps & Production Systems",
                "priority": "HIGH",
                "topics": [
                    "Feature stores: Feast, Vertex Feature Store — point-in-time correctness, online vs offline stores",
                    "Data versioning: DVC, Delta Lake — reproducibility without rerunning experiments",
                    "Pipeline orchestration: Kubeflow Pipelines, Vertex AI Pipelines, Apache Airflow for ML",
                    "Model registry: MLflow, Vertex AI Model Registry — versioning, staging, production promotion",
                    "Model monitoring: data drift (PSI, KL, Kolmogorov-Smirnov), concept drift alerts",
                    "Shadow deployment: run new model in shadow before promoting — catch failure modes safely",
                    "Cost optimization: spot instances for training, right-sizing, auto-scaling serving endpoints",
                ],
            },
        ],
    },
    {
        "label": "Phase 4",
        "weeks": "Weeks 12–13",
        "title": "Research Edge & Interview Supremacy",
        "weekly_hours": 76,
        "tagline": "The goal isn't to pass interviews. It's to be someone they'd be lucky to hire.",
        "milestone": "Top 10% Kaggle finish. Published technical blog or preprint. 3 portfolio projects on GitHub. All certs complete.",
        "goals": [
            "Complete 3 full ML system design mock interviews with recorded feedback",
            "Solve 80+ LeetCode (50 medium, 30 hard) — focus on graphs, DP, heaps",
            "Publish a technical blog post or arXiv preprint demonstrating original thinking",
            "Complete AWS ML Specialty exam",
            "Finalize GitHub portfolio: 3 polished projects with READMEs + notebooks",
        ],
        "domains": [
            {
                "name": "Research Fluency — Paper Command",
                "priority": "CRITICAL",
                "topics": [
                    "Attention Is All You Need (2017) — justify every architectural decision, propose improvements",
                    "BERT + GPT-1/2/3 — objectives, datasets, why each shaped a generation of NLP",
                    "Scaling Laws (Kaplan 2020 + Chinchilla 2022) — compute-optimal training, IsoFLOP curves",
                    "AlphaFold 2 — Evoformer, structure module, FAPE loss",
                    "DALL-E 2 + Stable Diffusion — CLIP alignment, latent diffusion, DDPM/DDIM sampling",
                    "LoRA (2021) + QLoRA (2023) — rank decomposition, NF4 quantization, memory analysis",
                    "Mamba (2023) — selective SSM, hardware-aware algorithm, why it challenges transformers",
                    "DeepSeek R1 / o1 reasoning — long chain-of-thought, test-time compute scaling",
                ],
            },
            {
                "name": "Coding Interviews — Elite Level",
                "priority": "CRITICAL",
                "topics": [
                    "LeetCode: 80+ problems — 50 medium, 30 hard. Patterns: sliding window, two pointers, monotonic stack",
                    "Graph algorithms: BFS/DFS, Dijkstra, Bellman-Ford, Topological sort, Tarjan SCC — implement cold",
                    "Dynamic programming: memoization vs tabulation, state design, 2D DP, interval DP, bitmask DP",
                    "Implement from scratch: k-means, logistic regression, decision tree, backprop, attention — in 20 mins",
                    "NumPy/JAX fluency: implement matrix ops, einsum notation, vmap usage — expect live numpy coding",
                    "System coding: design a distributed key-value store, implement LRU cache, rate limiter",
                ],
            },
            {
                "name": "ML System Design",
                "priority": "CRITICAL",
                "topics": [
                    "Design YouTube recommendation: two-tower model, candidate retrieval (ANN), ranking, diversity",
                    "Design real-time fraud detection: feature freshness, online learning, latency constraints",
                    "Design multimodal search (Google Lens): embedding pipeline, ANN index, reranking",
                    "Design LLM serving at 10M QPS: continuous batching, speculative decoding, KV cache management",
                    "Design A/B testing platform for ML models: traffic splitting, metric tracking, statistical power",
                    "Framework: problem framing → data → features → model choice → offline eval → online serving → monitoring",
                ],
            },
            {
                "name": "Portfolio Projects — Ship Three",
                "priority": "CRITICAL",
                "topics": [
                    "Project 1 — Research replication: replicate a 2023–2024 NLP/CV paper with improvements. Write blog post.",
                    "Project 2 — End-to-end ML system: data ingestion → training → serving → monitoring. Use Vertex AI or SageMaker.",
                    "Project 3 — Kaggle competition: document approach, feature engineering, ensemble strategy — top 10–20%.",
                    "All projects: clean README, Jupyter notebooks, reproducible Docker environments, performance benchmarks",
                    "Publish: arXiv preprint (even a 4-page technical report counts), Towards Data Science, or personal blog",
                ],
            },
        ],
    },
]

_RESOURCES = [
    # Phase 1 — Math & Classical ML
    {"phase": "phase-1", "title": "Pattern Recognition and Machine Learning", "author": "Christopher Bishop", "why": "The mathematical bible. Every proof matters. Do every exercise in Ch1–6.", "url": "https://microsoft.com/en-us/research/publication/pattern-recognition-machine-learning", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-1", "title": "The Elements of Statistical Learning (ESL)", "author": "Hastie, Tibshirani, Friedman", "why": "Deeper statistical treatment than Bishop. Essential for understanding SVMs, boosting, model selection.", "url": "https://web.stanford.edu/~hastie/ElemStatLearn", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-1", "title": "Mathematics for Machine Learning", "author": "Deisenroth, Faisal, Ong", "why": "Best single resource for linear algebra, multivariate calculus, and probability for ML. Read Ch2–6.", "url": "https://mml-book.github.io", "type": "book", "priority": "HIGH"},
    {"phase": "phase-1", "title": "Convex Optimization", "author": "Boyd & Vandenberghe", "why": "Chapters 1–5 are non-negotiable for anyone who wants to understand why optimization works.", "url": "https://stanford.edu/~boyd/cvxbook", "type": "book", "priority": "HIGH"},
    {"phase": "phase-1", "title": "Probabilistic Machine Learning (Vol 1 & 2)", "author": "Kevin Murphy", "why": "The modern successor to Bishop. Vol 2 covers deep generative models and advanced topics.", "url": "https://probml.github.io/pml-book", "type": "book", "priority": "HIGH"},
    {"phase": "phase-1", "title": "CS229: Machine Learning", "author": "Stanford (Andrew Ng)", "why": "The definitive ML course. Do the problem sets, not just the lectures. Problem sets 1–4 are your benchmark.", "url": "https://cs229.stanford.edu", "type": "course", "priority": "CRITICAL"},
    {"phase": "phase-1", "title": "XGBoost: A Scalable Tree Boosting System", "author": "Chen & Guestrin (2016)", "why": "Read this before using XGBoost. The second-order Taylor expansion section is the key insight.", "url": "https://arxiv.org/abs/1603.02754", "type": "paper", "priority": "HIGH"},
    {"phase": "phase-1", "title": "3Blue1Brown — Linear Algebra / Calculus series", "author": "3Blue1Brown", "why": "Best visual intuition builder for linear algebra and calculus. Watch before derivations.", "url": "https://youtube.com/c/3blue1brown", "type": "youtube", "priority": "HIGH"},
    {"phase": "phase-1", "title": "StatQuest with Josh Starmer", "author": "Josh Starmer", "why": "Best for classical ML intuition — decision trees, SVMs, PCA, regularization.", "url": "https://youtube.com/@statquest", "type": "youtube", "priority": "MEDIUM"},
    # Phase 2 — Deep Learning
    {"phase": "phase-2", "title": "Deep Learning", "author": "Goodfellow, Bengio, Courville", "why": "The textbook of record. Ch6–9 (feedforward, regularization, optimization, CNNs) are mandatory.", "url": "https://deeplearningbook.org", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "Dive into Deep Learning (D2L)", "author": "Zhang, Lipton, Li, Smola", "why": "Code-first textbook with runnable PyTorch/JAX/TF examples. Best for implementation alongside theory.", "url": "https://d2l.ai", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "Understanding Deep Learning", "author": "Simon J.D. Prince", "why": "2024's best new DL textbook. Exceptional coverage of diffusion models, flow matching, modern architectures.", "url": "https://udlbook.github.io/udlbook", "type": "book", "priority": "HIGH"},
    {"phase": "phase-2", "title": "CS231n: CNNs for Visual Recognition", "author": "Stanford", "why": "Best deep learning course for rigorous understanding. Assignments force true implementation mastery.", "url": "https://cs231n.stanford.edu", "type": "course", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "CS224N: NLP with Deep Learning", "author": "Stanford (Christopher Manning)", "why": "The NLP course. Transformers, attention, LLMs from the researchers who shaped the field.", "url": "https://web.stanford.edu/class/cs224n", "type": "course", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "fast.ai Practical Deep Learning", "author": "Jeremy Howard", "why": "Top-down learning style. Best for building intuition fast. Do Part 2 for the implementation depth.", "url": "https://course.fast.ai", "type": "course", "priority": "HIGH"},
    {"phase": "phase-2", "title": "Attention Is All You Need", "author": "Vaswani et al. (2017)", "why": "Read it 3 times. Justify every design decision. Know what was tried and rejected.", "url": "https://arxiv.org/abs/1706.03762", "type": "paper", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "BERT: Pre-training of Deep Bidirectional Transformers", "author": "Devlin et al. (2018)", "why": "Shaped NLP for 5 years. Understand MLM objective, NSP ablations, fine-tuning recipes.", "url": "https://arxiv.org/abs/1810.04805", "type": "paper", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "Language Models are Few-Shot Learners (GPT-3)", "author": "Brown et al. (2020)", "why": "Emergence of in-context learning. Scaling argument. The paper that changed everything.", "url": "https://arxiv.org/abs/2005.14165", "type": "paper", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "Denoising Diffusion Probabilistic Models", "author": "Ho et al. (2020)", "why": "Derive every equation. Implement DDPM from scratch. The foundation of modern image generation.", "url": "https://arxiv.org/abs/2006.11239", "type": "paper", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "Training language models to follow instructions (InstructGPT)", "author": "Ouyang et al. (2022)", "why": "The RLHF paper. Reward model training, PPO, KL penalty — all defined here.", "url": "https://arxiv.org/abs/2203.02155", "type": "paper", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "LoRA: Low-Rank Adaptation of Large Language Models", "author": "Hu et al. (2021)", "why": "The fine-tuning paper everyone uses. Rank decomposition, why it works, memory math.", "url": "https://arxiv.org/abs/2106.09685", "type": "paper", "priority": "HIGH"},
    {"phase": "phase-2", "title": "Direct Preference Optimization (DPO)", "author": "Rafailov et al. (2023)", "why": "Replaces PPO in many pipelines. Implicit reward derivation is elegant — derive it yourself.", "url": "https://arxiv.org/abs/2305.18290", "type": "paper", "priority": "HIGH"},
    {"phase": "phase-2", "title": "Andrej Karpathy — Neural Networks: Zero to Hero", "author": "Andrej Karpathy", "why": "Build micrograd, makemore, GPT-2 from scratch. The single best implementation series for deep learning.", "url": "https://youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "type": "youtube", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "Yannic Kilcher — Paper Walkthroughs", "author": "Yannic Kilcher", "why": "Best paper walkthrough channel. Watch every video on papers in your reading list. Deep, technical, opinionated.", "url": "https://youtube.com/@YannicKilcher", "type": "youtube", "priority": "CRITICAL"},
    {"phase": "phase-2", "title": "nanoGPT", "author": "Andrej Karpathy", "why": "Clean, minimal GPT-2 implementation. Read every line. Extend it. Your first training experiment.", "url": "https://github.com/karpathy/nanoGPT", "type": "tool", "priority": "CRITICAL"},
    # Phase 3 — Systems
    {"phase": "phase-3", "title": "Designing Machine Learning Systems", "author": "Chip Huyen", "why": "The MLOps bible. Every chapter is directly testable in senior interviews. Read cover to cover.", "url": "https://oreilly.com/library/view/designing-machine-learning/9781098107956", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-3", "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "why": "Not ML-specific but mandatory for senior engineers. Distributed systems, consistency, replication.", "url": "https://dataintensive.net", "type": "book", "priority": "HIGH"},
    {"phase": "phase-3", "title": "MLOps Specialization", "author": "deeplearning.ai (Andrew Ng, Laurence Moroney)", "why": "4-course series on production ML. Feature stores, model monitoring, CI/CD, data validation.", "url": "https://deeplearning.ai/courses/machine-learning-engineering-for-production-mlops", "type": "course", "priority": "CRITICAL"},
    {"phase": "phase-3", "title": "Full Stack Deep Learning", "author": "FSDL (Josh Tobin, Pieter Abbeel et al.)", "why": "End-to-end ML system design. Labs build a real product. Best practical systems course.", "url": "https://fullstackdeeplearning.com", "type": "course", "priority": "CRITICAL"},
    {"phase": "phase-3", "title": "JAX: Accelerated Machine Learning Research", "author": "Bradbury et al. (Google, 2018)", "why": "The JAX paper. Understand the design philosophy before writing code.", "url": "https://github.com/google/jax", "type": "paper", "priority": "CRITICAL"},
    {"phase": "phase-3", "title": "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models", "author": "Rajbhandari et al. (2020)", "why": "ZeRO-1/2/3 optimizer state sharding. Why DeepSpeed exists. Understand stages before using.", "url": "https://arxiv.org/abs/1910.02054", "type": "paper", "priority": "HIGH"},
    {"phase": "phase-3", "title": "Hidden Technical Debt in Machine Learning Systems", "author": "Sculley et al. (Google, 2015)", "why": "The MLOps manifesto. Every senior ML engineer must have internalized this paper's lessons.", "url": "https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba", "type": "paper", "priority": "HIGH"},
    {"phase": "phase-3", "title": "Weights & Biases", "author": "Weights & Biases", "why": "Industry-standard experiment tracking. Learn it cold — sweeps, artifacts, reports. Free for individuals.", "url": "https://wandb.ai", "type": "tool", "priority": "CRITICAL"},
    {"phase": "phase-3", "title": "vLLM", "author": "UC Berkeley Sky Lab", "why": "PagedAttention-based LLM serving. Read the codebase. Benchmark it. Know the internals.", "url": "https://github.com/vllm-project/vllm", "type": "tool", "priority": "HIGH"},
    # Phase 4 — Research & Interviews
    {"phase": "phase-4", "title": "Cracking the ML Interview", "author": "Khang Pham", "why": "Most complete ML interview prep book. Covers theory Q&A, system design, coding. Keep it close.", "url": "https://amazon.com/dp/B09R2M7KN3", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-4", "title": "LeetCode", "author": "LeetCode", "why": "Non-negotiable. 80+ problems. Focus: graphs (20), DP (25), heaps/priority queues (10), sliding window (10).", "url": "https://leetcode.com", "type": "tool", "priority": "CRITICAL"},
    {"phase": "phase-4", "title": "Kaggle Competitions", "author": "Kaggle", "why": "Start Week 1. One competition always active. Top 10% on any featured competition is resume gold.", "url": "https://kaggle.com/competitions", "type": "tool", "priority": "CRITICAL"},
    {"phase": "phase-4", "title": "Papers With Code", "author": "Papers With Code", "why": "Track SOTA benchmarks, find reference implementations, stay current. Use daily from Week 1.", "url": "https://paperswithcode.com", "type": "tool", "priority": "HIGH"},
    {"phase": "phase-4", "title": "Lil'Log", "author": "Lilian Weng (OpenAI)", "why": "The best ML blog on the internet. Every post is a masterclass. Diffusion, attention, RL — all covered deeply.", "url": "https://lilianweng.github.io", "type": "book", "priority": "CRITICAL"},
    {"phase": "phase-4", "title": "Jay Alammar's Blog — The Illustrated Transformer", "author": "Jay Alammar", "why": "Best visual explanations of transformers, BERT, GPT. 'The Illustrated Transformer' is essential.", "url": "https://jalammar.github.io", "type": "book", "priority": "HIGH"},
    {"phase": "phase-4", "title": "Mamba: Linear-Time Sequence Modeling with Selective State Spaces", "author": "Gu & Dao (2023)", "why": "The transformer challenger. Selective SSM, hardware-aware design. Know it to critique it.", "url": "https://arxiv.org/abs/2312.00752", "type": "paper", "priority": "HIGH"},
]


async def seed_roadmap(user_id: str = USER_ID) -> None:
    """Seed ML roadmap items. Idempotent — skips if already seeded."""
    existing = await list_items(user_id)
    if any("ml-roadmap" in (it.tags or []) for it in existing):
        print("ML Roadmap already seeded — skipping.")
        return

    count = 0

    # Certifications
    for cert in _CERTIFICATIONS:
        slug = cert["provider"].lower().replace(" ", "-").replace("/", "-")
        item = Item(
            user_id=user_id,
            state=ItemState.backlog,
            type=ItemType.resource,
            title=cert["name"],
            content=f"{cert['desc']}\n\nTimeline: {cert['duration']} | Effort: {cert['effort']} | Value: {cert['salary']}",
            tags=["ml-roadmap", "certification", slug],
            source_url=cert["url"],
            effort_estimate=cert["effort"],
        )
        await save_item(item)
        count += 1

    # Phases — summary items + domain items
    for phase in _PHASES:
        phase_slug = phase["label"].lower().replace(" ", "-")
        goals_text = "\n".join(f"• {g}" for g in phase["goals"])

        # Phase summary item
        phase_item = Item(
            user_id=user_id,
            state=ItemState.backlog,
            type=ItemType.topic,
            title=f"{phase['label']}: {phase['title']}",
            content=f"{phase['tagline']}\n\n{phase['weeks']} | {phase['weekly_hours']} hrs/week\n\nMilestone: {phase['milestone']}\n\nGoals:\n{goals_text}",
            tags=["ml-roadmap", phase_slug, "curriculum", "phase-overview"],
            effort_estimate=phase["weeks"],
        )
        await save_item(phase_item)
        count += 1

        # Domain items
        for domain in phase["domains"]:
            topics_text = "\n".join(f"• {t}" for t in domain["topics"])
            domain_item = Item(
                user_id=user_id,
                state=ItemState.backlog,
                type=ItemType.topic,
                title=domain["name"],
                content=topics_text,
                tags=["ml-roadmap", phase_slug, "domain", domain["priority"].lower()],
                effort_estimate=phase["weeks"],
            )
            await save_item(domain_item)
            count += 1

    # Resources
    _type_map = {"paper": ItemType.paper, "book": ItemType.resource, "course": ItemType.resource, "youtube": ItemType.resource, "tool": ItemType.resource}
    for res in _RESOURCES:
        item = Item(
            user_id=user_id,
            state=ItemState.backlog,
            type=_type_map.get(res["type"], ItemType.resource),
            title=res["title"],
            content=f"{res['why']}\n\nAuthor: {res['author']}",
            tags=["ml-roadmap", res["phase"], "resource", res["type"], res["priority"].lower()],
            source_url=res.get("url"),
            effort_estimate=res["priority"],
        )
        await save_item(item)
        count += 1

    print(f"✅ Seeded {count} ML Roadmap items for user '{user_id}'.")
