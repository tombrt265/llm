import numpy as np

def generate_cbow_pairs(words, window_size=2):
    """Generate all CBOW (context, target) training pairs from a sequence of words."""
    pairs = []
    for target_idx in range(len(words)):
        context = []
        for offset in range(-window_size, window_size + 1):
            if offset == 0:
                continue
            context_idx = target_idx + offset
            if 0 <= context_idx < len(words):
                context.append(words[context_idx])
        if context:  # Only include positions with at least one context word
            pairs.append((context, words[target_idx]))
    return pairs


def softmax(x):
    """Numerically stable softmax."""
    x = x - np.max(x)  # Subtract max for numerical stability
    e_x = np.exp(x)
    return e_x / e_x.sum()


def cbow_forward(context_words, W, W_prime, word_to_idx):
    """
    CBOW forward pass.
    Returns averaged hidden representation and softmax probabilities.
    """
    # Step 1: Look up embeddings for context words
    context_embs = np.array([W[word_to_idx[w]] for w in context_words])

    # Step 2: Average context embeddings
    h_bar = np.mean(context_embs, axis=0)

    # Step 3: Compute output scores
    scores = W_prime.T @ h_bar

    # Step 4: Apply softmax
    probs = softmax(scores)

    return h_bar, probs


def cbow_backward(
    context_words, target_word, h_bar, probs, W, W_prime, word_to_idx
):
    """
    CBOW backward pass. Returns parameter gradients.
    """
    V = W_prime.shape[1]
    target_idx = word_to_idx[target_word]

    # Step 1: Prediction error (softmax gradient)
    e = probs.copy()
    e[target_idx] -= 1.0  # Subtract 1 from the correct word

    # Step 2: Gradient for W_prime
    dW_prime = np.outer(h_bar, e)  # shape: (d, V)

    # Step 3: Gradient for hidden representation
    dh_bar = W_prime @ e  # shape: (d,)

    # Step 4: Gradient for embedding matrix (distribute equally to all context words)
    dW = np.zeros_like(W)
    C = len(context_words)
    for word in context_words:
        dW[word_to_idx[word]] += dh_bar / C

    return dW, dW_prime


def compute_loss(target_word, probs, word_to_idx):
    """Negative log-likelihood loss."""
    return -np.log(probs[word_to_idx[target_word]] + 1e-10)


def train_cbow(
    corpus_words,
    vocab,
    word_to_idx,
    embedding_dim=8,
    window_size=2,
    learning_rate=0.01,
    epochs=200,
):
    """
    Train a CBOW model using stochastic gradient descent.
    Returns the trained embedding matrix.
    """
    V = len(vocab)
    np.random.seed(42)
    W_emb = np.random.randn(V, embedding_dim) * 0.01
    W_out = np.random.randn(embedding_dim, V) * 0.01

    # Generate all training pairs
    pairs = generate_cbow_pairs(corpus_words, window_size)

    losses = []

    for epoch in range(epochs):
        epoch_loss = 0.0
        np.random.shuffle(pairs)

        for context_words, target_word in pairs:
            # Forward pass
            h_bar, probs = cbow_forward(
                context_words, W_emb, W_out, word_to_idx
            )
            loss = compute_loss(target_word, probs, word_to_idx)
            epoch_loss += loss

            # Backward pass
            dW, dW_prime = cbow_backward(
                context_words,
                target_word,
                h_bar,
                probs,
                W_emb,
                W_out,
                word_to_idx,
            )
            # Update parameters
            W_emb -= learning_rate * dW
            W_out -= learning_rate * dW_prime

        losses.append(epoch_loss / len(pairs))

    return W_emb, W_out, losses

