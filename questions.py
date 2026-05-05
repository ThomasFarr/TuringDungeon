"""
questions.py  —  CS305 Theory of Computation question bank
Each question: q=question text, c=choices list (4), a=answer index (0-3), e=explanation

24 regular questions per topic, ordered easy → hard:
  easy   tier : indices  0-7   (definitions, recall)
  medium tier : indices  5-12  (comprehension, application; 3-Q overlap with easy at 5-7)
  hard   tier : indices 10-23  (analysis, synthesis; 3-Q overlap with medium at 10-12)

Former "boss" questions are at indices 12-14; hard extension questions at 18-23.
"""

TOPICS = {
    "DFA":   "Deterministic Finite Automata",
    "NFA":   "Nondeterministic Finite Automata",
    "ENFA":  "Epsilon-NFA  (ε-NFA)",
    "REGEX": "Regular Expressions",
    "PUMP":  "Pumping Theorem",
    "CFG":   "Context-Free Grammars",
    "PDA":   "Pushdown Automata",
    "TM":    "Turing Machines",
    "UTM":   "Universal Turing Machine",
    "PNP":   "P vs NP",
}

TOPIC_ORDER = list(TOPICS.keys())

QUESTION_BANK = {

    # ───────────────────────────── DFA ─────────────────────────────
    "DFA": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "What does DFA stand for?",
                "c": ["Dynamic Function Automaton", "Deterministic Finite Automaton",
                      "Discrete Formal Algorithm", "Defined Finite Automaton"],
                "a": 1,
                "e": "DFA = Deterministic Finite Automaton. 'Deterministic' means exactly one transition per state per input symbol.",
                "ce": "DFA stands for Deterministic Finite Automaton, where δ gives exactly one next state per symbol."
            },
            {
                "q": "A DFA is formally defined as a 5-tuple. Which option lists the correct components?",
                "c": ["(Q, Σ, δ, q₀, F)", "(Q, Σ, γ, s, A)", "(S, Σ, δ, q₀, R)", "(V, T, P, S, F)"],
                "a": 0,
                "e": "A DFA is (Q, Σ, δ, q₀, F): states, alphabet, transition function, start state, accept states.",
                "ce": "(Q, Σ, δ, q₀, F) is the standard DFA 5-tuple: states, alphabet, transition function, start state, accept states."
            },
            {
                "q": "How many transitions must exist for each state and each input symbol in a DFA?",
                "c": ["Zero or one", "Exactly one", "One or more", "Any number"],
                "a": 1,
                "e": "The DFA transition function δ: Q×Σ→Q is total — exactly one next state for every (state, symbol) pair.",
                "ce": "δ: Q×Σ→Q is a total function, so exactly one next state exists for every state-symbol pair."
            },
            {
                "q": "The transition function δ of a DFA maps...",
                "c": ["Q → Σ", "Q × Σ → 2^Q", "Q × Σ → Q", "Σ* → Q"],
                "a": 2,
                "e": "δ: Q×Σ→Q — given a state and input symbol, it returns exactly one next state.",
                "ce": "δ: Q×Σ→Q maps each (state, symbol) pair to exactly one next state."
            },
            {
                "q": "A string w is accepted by a DFA if...",
                "c": ["Some path through δ ends in F", "δ*(q₀, w) ∈ F", "w ∈ Σ*", "q₀ ∈ F"],
                "a": 1,
                "e": "The extended transition function δ* processes the entire string from q₀; if the final state is in F, the string is accepted.",
                "ce": "w is accepted iff δ*(q₀, w) ∈ F, meaning the unique final state after processing w from q₀ is accepting."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "What is a 'trap state' (dead state) in a DFA?",
                "c": ["The start state", "An accept state with no outgoing transitions",
                      "A non-accept state where all transitions loop back to itself", "Any state not reachable from q₀"],
                "a": 2,
                "e": "A trap/dead state is a non-accepting state that absorbs all future input — once entered, the machine can never accept.",
                "ce": "a trap (dead) state is a non-accepting sink: all transitions loop back to itself, making acceptance impossible."
            },
            {
                "q": "What does the extended transition function δ* compute?",
                "c": ["The number of transitions taken", "The state reached after processing an entire string",
                      "The set of all reachable states", "The length of the accepted string"],
                "a": 1,
                "e": "δ*(q, w) extends δ to strings: δ*(q, ε)=q and δ*(q, wa)=δ(δ*(q,w), a).",
                "ce": "δ*(q, w) gives the unique state reached by processing the entire string w symbol-by-symbol from state q."
            },
            {
                "q": "Can a DFA have multiple start states?",
                "c": ["Yes, that is what makes it nondeterministic", "Yes, as long as they are all accept states",
                      "No — a DFA has exactly one start state q₀", "Only if the alphabet has more than one symbol"],
                "a": 2,
                "e": "A DFA has exactly one start state q₀. Multiple start states would make it nondeterministic.",
                "ce": "q₀ is unique in a DFA; multiple start states would introduce nondeterminism."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "DFAs recognize exactly which class of languages?",
                "c": ["Context-free languages", "Regular languages", "Recursively enumerable languages", "Decidable languages"],
                "a": 1,
                "e": "DFAs (and NFAs and regular expressions) all recognize exactly the regular languages.",
                "ce": "DFAs recognize exactly the regular languages, as established by Kleene's theorem."
            },
            {
                "q": "The Myhill-Nerode theorem is primarily used to...",
                "c": ["Convert NFAs to DFAs", "Prove a language is context-free",
                      "Minimize DFAs and determine if a language is regular", "Construct a universal Turing machine"],
                "a": 2,
                "e": "The Myhill-Nerode theorem characterizes regularity via equivalence classes of strings and gives the minimum-state DFA.",
                "ce": "Myhill-Nerode characterizes regularity via right-congruence classes and directly yields the minimal DFA."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "Two DFA states p and q are 'distinguishable' if...",
                "c": ["They have the same transitions", "There exists a string x such that exactly one of δ*(p,x), δ*(q,x) is in F",
                      "They are both accept states", "They are unreachable from q₀"],
                "a": 1,
                "e": "States are distinguishable if some string separates them — one reaches an accept state and the other does not.",
                "ce": "p and q are distinguishable if some witness string x produces different acceptance outcomes from each state."
            },
            {
                "q": "Can a DFA have zero accept states?",
                "c": ["No — every DFA must accept at least one string", "Yes — it would accept the empty language ∅",
                      "Only if the alphabet is empty", "Only if all states are start states"],
                "a": 1,
                "e": "Yes. A DFA with F=∅ accepts no strings, recognizing the empty language ∅, which is regular.",
                "ce": "F=∅ means no state is accepting, so no string is ever accepted, which recognizes the empty language ∅."
            },
            {
                "q": "Which of the following languages CANNOT be recognized by any DFA?",
                "c": ["{w | w contains the substring 'ab'}", "{a^n b^n | n ≥ 0}",
                      "{w | w ends in 0}", "{w ∈ {a,b}* | w has even length}"],
                "a": 1,
                "e": "{a^n b^n} requires counting (matching a's with b's) — a DFA has finite memory and cannot count arbitrarily.",
                "ce": "{a^n b^n} requires counting and matching equal numbers of a's and b's, which exceeds DFA capabilities."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "A DFA M has n states. The minimum-state equivalent DFA is obtained by...",
                "c": ["Removing all unreachable states and merging indistinguishable states via the table-filling algorithm",
                      "Reversing all transitions and re-determinizing",
                      "Converting to an NFA first, then back to a DFA",
                      "Adding a dead state and removing ε-transitions"],
                "a": 0,
                "e": "DFA minimization: remove unreachable states, then merge all pairs of indistinguishable states (table-filling/Hopcroft's algorithm).",
                "ce": "DFA minimization: remove unreachable states, then apply table-filling to find and merge all indistinguishable state pairs."
            },
            {
                "q": "Given DFA M, the complement language L(M)^c is recognized by which machine?",
                "c": ["A new DFA with all transitions reversed",
                      "The DFA M with accept and non-accept states swapped",
                      "An NFA with ε-transitions added",
                      "A PDA that simulates M on a stack"],
                "a": 1,
                "e": "Swapping F and Q\\F in a complete DFA gives a DFA for the complement — regular languages are closed under complement.",
                "ce": "swapping F and Q∖F in a complete DFA gives a DFA that accepts exactly what the original rejected."
            },
            {
                "q": "Given DFA M₁ with n₁ states and DFA M₂ with n₂ states, the product construction for L(M₁) ∩ L(M₂) yields a DFA with at most how many states?",
                "c": ["n₁ + n₂", "n₁ × n₂", "2^(n₁ + n₂)", "n₁ · |Σ| + n₂ · |Σ|"],
                "a": 1,
                "e": "The product construction uses pairs (q₁, q₂) ∈ Q₁ × Q₂ as states, giving at most n₁ × n₂ states.",
                "ce": "the product construction pairs every state from M₁ with every state from M₂, giving at most n₁ × n₂ states."
            },
            {
                "q": "The Myhill-Nerode theorem states that the number of equivalence classes of ≡_L equals...",
                "c": ["The number of states in any DFA for L",
                      "The number of states in the minimum-state DFA for L",
                      "The pumping length of L",
                      "The number of accept states in the minimal DFA"],
                "a": 1,
                "e": "The index of ≡_L (number of right-invariant equivalence classes) exactly equals the state count of the unique minimal DFA.",
                "ce": "the Myhill-Nerode theorem states the index of ≡_L equals the state count of the unique minimal DFA."
            },
            {
                "q": "A DFA for the reversal language L^R = {w^R | w ∈ L} can be constructed by...",
                "c": ["Reversing all transitions, making original accept states the new start states, and applying the subset construction",
                      "Swapping accept and non-accept states in the original DFA",
                      "Reading the input right-to-left in the original DFA without modification",
                      "Adding ε-transitions from every state back to q₀"],
                "a": 0,
                "e": "Reverse all edges, the original accept states become start states (use a new ε-start if multiple), then determinize via subset construction.",
                "ce": "reversing all edges and swapping start/accept roles creates an NFA for L^R; subset construction then determinizes it."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "The Myhill-Nerode theorem states that a language L is regular if and only if...",
                "c": ["L is accepted by some DFA with at most 100 states",
                      "The relation x≡_L y (defined by: ∀z, xz∈L⇔yz∈L) has finitely many equivalence classes",
                      "L can be defined by a regular expression without Kleene star",
                      "L has at most polynomially many strings"],
                "a": 1,
                "e": "Myhill-Nerode: L is regular iff the right-congruence ≡_L has finitely many equivalence classes. The class count equals the minimal DFA state count.",
                "ce": "Myhill-Nerode: L is regular iff the right-congruence ≡_L (x≡y iff ∀z, xz∈L⟺yz∈L) has finitely many classes."
            },
            {
                "q": "In DFA table-filling (Hopcroft) minimization, two states p and q are 'distinguishable' if...",
                "c": ["They have different numbers of outgoing transitions",
                      "There exists a string w such that exactly one of δ*(p,w), δ*(q,w) is an accepting state",
                      "p is an accepting state and q is not (without any further string)",
                      "They are not directly connected by any transition"],
                "a": 1,
                "e": "States p and q are distinguishable if some string w separates them: δ*(p,w)∈F XOR δ*(q,w)∈F. The algorithm initializes accept/non-accept pairs, then propagates backwards.",
                "ce": "p and q are distinguishable iff some string w leads one to an accept state and the other to a non-accept state."
            },
            {
                "q": "To build a DFA for L₁ ∩ L₂ via the product construction, if M₁ has m states and M₂ has n states, the resulting DFA has at most...",
                "c": ["m + n states", "m × n states (one per pair of states from M₁ and M₂)",
                      "2^(m+n) states", "max(m, n) states"],
                "a": 1,
                "e": "Product construction: states are pairs (q₁, q₂). Transitions: δ((q₁,q₂), a) = (δ₁(q₁,a), δ₂(q₂,a)). Accept states: pairs where both components accept. Worst case: m×n states.",
                "ce": "states are pairs (q₁, q₂) ∈ Q₁ × Q₂; with m and n states, there are at most m × n pairs."
            },
            {
                "q": "The complement of a regular language over alphabet Σ is always...",
                "c": ["Context-free but not necessarily regular",
                      "Regular — swap accepting and non-accepting states in the complete DFA",
                      "Undecidable in general",
                      "Only regular if the original language is finite"],
                "a": 1,
                "e": "Regular languages are closed under complement: given a complete DFA for L, swapping F and Q∖F gives a DFA for Σ*∖L. The DFA must be complete (a dead state for every missing transition).",
                "ce": "swap F and Q∖F in a complete DFA; regular languages are closed under complement."
            },
            {
                "q": "The pumping length p in the Pumping Lemma for a regular language L corresponds to...",
                "c": ["The length of the longest string in L",
                      "The number of states in a DFA for L — any string of length ≥ p must visit a repeated state by pigeonhole",
                      "The number of accepting states in the minimal DFA for L",
                      "The index of the hardest question in the quiz"],
                "a": 1,
                "e": "Setting p = number of DFA states: processing a string of length ≥ p visits at least p+1 states. By pigeonhole, some state repeats, creating the pumpable loop xy.",
                "ce": "p equals the DFA state count; reading ≥ p symbols visits ≥ p+1 states, forcing a repeated state by pigeonhole."
            },
            {
                "q": "The 'state complexity' of the union L₁ ∪ L₂ when the minimal DFAs have m and n states respectively is at most...",
                "c": ["m + n states", "m × n states",
                      "(m+1)(n+1) states — accounting for a possible dead state in each DFA",
                      "2^m + 2^n states"],
                "a": 1,
                "e": "Product construction for union: accept states are pairs where at least one component accepts. Worst case m×n. The (m+1)(n+1) bound applies when we include the implicit dead state of each complete DFA.",
                "ce": "product construction for union uses pairs (q₁, q₂); accept pairs are those where at least one component is accepting."
            },
        ],
    },

    # ───────────────────────────── NFA ─────────────────────────────
    "NFA": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "How does an NFA differ from a DFA?",
                "c": ["An NFA can only have one accept state", "An NFA can have zero or multiple transitions per state per symbol",
                      "An NFA cannot have a start state", "An NFA reads input right-to-left"],
                "a": 1,
                "e": "In an NFA, δ(q, a) can return the empty set (no transition) or multiple next states.",
                "ce": "δ(q, a) returns a set (possibly empty, possibly with multiple states), unlike DFA's single-state return."
            },
            {
                "q": "The transition function of an NFA maps to...",
                "c": ["Q", "Q × Σ", "2^Q (the power set of Q)", "Σ*"],
                "a": 2,
                "e": "δ: Q×Σ→2^Q — it returns a set of states (possibly empty) instead of a single state.",
                "ce": "δ: Q×Σ→2^Q returns a subset of Q (the power set), allowing zero or multiple next states."
            },
            {
                "q": "An NFA accepts a string w if...",
                "c": ["All computation paths end in accept states", "At least one computation path ends in an accept state",
                      "The majority of paths end in accept states", "The first path tried ends in an accept state"],
                "a": 1,
                "e": "NFA acceptance is existential — if any possible computation path leads to an accept state, the string is accepted.",
                "ce": "NFA acceptance is existential: if at least one computation path ends in an accept state, the string is accepted."
            },
            {
                "q": "The subset construction (powerset construction) converts an NFA to...",
                "c": ["A context-free grammar", "An equivalent DFA",
                      "A pushdown automaton", "A Turing machine"],
                "a": 1,
                "e": "The subset construction creates a DFA whose states are subsets of the NFA's state set.",
                "ce": "the subset (powerset) construction converts an NFA to an equivalent DFA by tracking sets of NFA states."
            },
            {
                "q": "An NFA with n states may require a DFA with at most how many states?",
                "c": ["n states", "n² states", "2n states", "2^n states"],
                "a": 3,
                "e": "Each subset of the NFA's n states becomes a potential DFA state, giving at most 2^n DFA states.",
                "ce": "the power set of n NFA states has 2^n subsets, each a potential DFA state."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "NFAs and DFAs are equivalent in the sense that...",
                "c": ["They have the same number of states for any language",
                      "They recognize exactly the same class of languages (regular)",
                      "They both run in polynomial time", "They both require the same number of transitions"],
                "a": 1,
                "e": "NFAs and DFAs recognize exactly the regular languages — nondeterminism adds no power here.",
                "ce": "NFAs and DFAs recognize exactly the same class of languages (regular languages), proven by the subset construction."
            },
            {
                "q": "What makes NFAs useful in practice if they are not more powerful than DFAs?",
                "c": ["They are faster to simulate on hardware", "They can be smaller and easier to design for certain languages",
                      "They do not require a start state", "They can recognize non-regular languages"],
                "a": 1,
                "e": "NFAs can be exponentially more compact than equivalent DFAs and are often easier to construct.",
                "ce": "NFAs can be exponentially smaller than equivalent DFAs and are often more natural to design."
            },
            {
                "q": "In the subset construction, the start state of the resulting DFA is...",
                "c": ["An empty set ∅", "The set of all NFA states Q",
                      "The set containing only the NFA's start state {q₀}", "Any accept state of the NFA"],
                "a": 2,
                "e": "The DFA starts in the state {q₀}, representing the NFA beginning in its single start state.",
                "ce": "the DFA start state is {q₀}, the singleton set containing only the NFA's start state."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "Which subsets of NFA states become accept states of the DFA in the subset construction?",
                "c": ["Only the subset containing all NFA accept states",
                      "Any subset containing at least one NFA accept state",
                      "Only subsets containing exactly one accept state", "The empty set ∅"],
                "a": 1,
                "e": "A DFA state (a subset S of NFA states) is accepting if S ∩ F ≠ ∅ — i.e., it contains at least one NFA accept state.",
                "ce": "any DFA subset-state S is accepting if S ∩ F ≠ ∅, meaning it contains at least one NFA accept state."
            },
            {
                "q": "An NFA rejects a string w if...",
                "c": ["The NFA's start state is non-accepting",
                      "All computation paths end in non-accept states or get stuck (dead ends)",
                      "w is the empty string", "The NFA has more than one start state"],
                "a": 1,
                "e": "Rejection means every computation path either gets stuck (no transition) or ends in a non-accept state.",
                "ce": "an NFA rejects w only when all computation paths are exhausted without any reaching an accept state."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "In an NFA, what happens if the machine is in state q and reads symbol a with δ(q,a)=∅?",
                "c": ["The machine crashes", "That computation path dies (is rejected)",
                      "The machine loops forever", "The machine accepts immediately"],
                "a": 1,
                "e": "When δ(q,a)=∅, that branch of computation has no successor — it dies (rejects). Other branches may still continue.",
                "ce": "δ(q,a)=∅ means that branch dies (no next state), but other parallel branches may still reach an accept state."
            },
            {
                "q": "The powerset construction produces a DFA with states drawn from...",
                "c": ["All strings in Σ*", "All pairs of NFA states",
                      "All subsets of the NFA state set Q", "All transitions of the NFA"],
                "a": 2,
                "e": "States in the subset-construction DFA are elements of 2^Q — every subset of NFA states is a candidate DFA state.",
                "ce": "the DFA's state set is drawn from 2^Q, the power set of all NFA states."
            },
            {
                "q": "Why does the subset construction sometimes produce exponentially many DFA states in practice?",
                "c": ["NFAs always have exponentially more transitions than DFAs",
                      "Each subset of NFA states is a potential DFA state; with n NFA states there are 2^n possible subsets",
                      "DFAs require one state per input symbol", "The NFA alphabet is always larger than the DFA alphabet"],
                "a": 1,
                "e": "The 2^n worst-case occurs for certain NFAs (e.g., 'strings whose n-th-from-last character is 1') where nearly all subsets are reachable.",
                "ce": "with n NFA states, all 2^n subsets are potential DFA states, and for some NFAs nearly all are reachable."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "The equivalence of NFAs and DFAs (recognizing the same languages) proves...",
                "c": ["NFAs are always faster than DFAs", "Nondeterminism adds no computational power for language recognition",
                      "Every regular language requires exponential DFA states", "NFAs can recognize context-free languages"],
                "a": 1,
                "e": "The closure under subset construction shows that nondeterminism is a design convenience, not extra power, for finite automata.",
                "ce": "NFA/DFA equivalence shows nondeterminism adds no language-recognition power for finite automata."
            },
            {
                "q": "An NFA for the language {w ∈ {0,1}* | the 3rd-from-last symbol is 1} has 4 states. The equivalent DFA has...",
                "c": ["4 states", "8 states", "exactly 2^4 = 16 states", "an unbounded number of states"],
                "a": 2,
                "e": "This is a classic example where all 2^n subsets are reachable in the subset construction — the DFA requires exactly 2^n states.",
                "ce": "this language requires exactly 2^4 = 16 DFA states, as all 2^n subsets are reachable."
            },
            {
                "q": "In the lazy (on-the-fly) subset construction only reachable DFA states are computed. For an NFA with n states, the number of reachable subsets is...",
                "c": ["Always exactly 2^n", "At most 2^n (often far fewer in practice)",
                      "Always exactly n + 1", "Always exactly n²"],
                "a": 1,
                "e": "Only reachable subsets matter — worst case is 2^n but many NFAs yield far fewer reachable subsets, making lazy construction practical.",
                "ce": "at most 2^n reachable subsets, but in practice many NFAs have far fewer reachable DFA states."
            },
            {
                "q": "To build an NFA for the concatenation L₁L₂, given NFAs M₁ and M₂, the construction...",
                "c": ["Takes the cross product of M₁ and M₂",
                      "Adds ε-transitions from each accept state of M₁ to the start state of M₂, making M₁'s accept states non-accepting in the combined machine",
                      "Runs M₁ and M₂ in parallel on the same input",
                      "Reverses M₂ and composes it with M₁"],
                "a": 1,
                "e": "Concatenation NFA: M₁ followed by M₂, connected by ε-transitions from M₁'s old accept states to M₂'s start state. M₁'s accept states lose their accepting status.",
                "ce": "ε-transitions from M₁'s accept states to M₂'s start state chain the machines; M₁'s old accept states become non-accepting."
            },
            {
                "q": "An NFA that recognizes {w ∈ {0,1}* | the k-th-to-last symbol is 1} requires a minimal DFA with how many states?",
                "c": ["k + 1 states", "2k states", "2^k states", "k² states"],
                "a": 2,
                "e": "This family requires 2^k DFA states — nearly all subsets of the k-state NFA are reachable, giving the canonical exponential blowup example.",
                "ce": "the minimal DFA requires exactly 2^k states because all subsets of the k-state NFA are reachable."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "The subset construction converting an NFA with n states to a DFA can produce at most how many states?",
                "c": ["n states", "n² states", "2ⁿ states (one per subset of NFA states)",
                      "n! states"],
                "a": 2,
                "e": "The subset construction's states are subsets of the NFA state set. With n states, there are 2ⁿ subsets. This worst case is tight — e.g., the language where the k-th-from-last symbol is 1 requires exactly 2^k DFA states.",
                "ce": "the DFA has at most 2^n states (one per subset of NFA states), and this bound is tight for certain languages."
            },
            {
                "q": "Deciding whether an NFA accepts at least one string (non-emptiness) can be done in...",
                "c": ["Exponential time (must convert to DFA first)",
                      "Polynomial time — graph reachability: is any accept state reachable from q₀?",
                      "Only by exhaustive search over Σ*",
                      "Linear time only if the NFA is deterministic"],
                "a": 1,
                "e": "NFA non-emptiness = directed reachability. BFS/DFS from q₀ over ε-closure and transitions. If any accept state is reachable, L(NFA) ≠ ∅. Runs in O(|Q|+|δ|) time.",
                "ce": "NFA non-emptiness is reachability: BFS/DFS from q₀ to check if any accept state is reachable, in O(|Q|+|δ|) time."
            },
            {
                "q": "Deciding whether an NFA accepts ALL strings over Σ* (universality) is...",
                "c": ["Polynomial time via graph reachability",
                      "Polynomial time by checking the complement NFA is empty",
                      "PSPACE-complete — exponentially harder than NFA non-emptiness",
                      "Undecidable"],
                "a": 2,
                "e": "NFA universality is PSPACE-complete. Checking requires converting the complement NFA to a DFA (exponential in general). No polynomial-time or polynomial-space algorithm is known.",
                "ce": "NFA universality is PSPACE-complete, requiring exponential work in general (e.g., via DFA conversion)."
            },
            {
                "q": "To construct an NFA for the reversal Lᴿ of a regular language L given DFA M, we...",
                "c": ["Cannot — reversal of a regular language may not be regular",
                      "Reverse all transitions, make old start state the single accept state, add a new start with ε-transitions to all old accept states",
                      "Reverse the alphabetical order of all transitions",
                      "Complement the DFA and reverse the input"],
                "a": 1,
                "e": "Reversal NFA construction: reverse all edges, swap roles of start and accept. Old accept states merge into a new start via ε-transitions; old start becomes the sole accept. Regular languages are closed under reversal.",
                "ce": "reverse all edges, make old start state the sole accept, add a new start with ε-edges to all old accept states."
            },
            {
                "q": "Which statement best captures the relationship between NFAs and DFAs in terms of expressive power?",
                "c": ["NFAs recognize strictly more languages than DFAs",
                      "DFAs recognize strictly more languages than NFAs",
                      "NFAs and DFAs recognize exactly the same class (regular languages), but NFAs can be exponentially more succinct",
                      "NFAs can only recognize finite languages"],
                "a": 2,
                "e": "By the subset construction every NFA has an equivalent DFA — same power. However, the DFA may need exponentially more states. This succinctness gap is real and tight.",
                "ce": "NFAs and DFAs recognize the same class (regular languages), but NFAs can be exponentially more succinct."
            },
            {
                "q": "Adding ε-transitions to NFAs (creating ε-NFAs) compared to plain NFAs...",
                "c": ["Increases the class of recognizable languages beyond regular",
                      "Only allows recognition of ε",
                      "Does not increase expressive power — every ε-NFA is equivalent to an NFA without ε-transitions",
                      "Doubles the maximum number of states needed"],
                "a": 2,
                "e": "ε-NFAs are equivalent to NFAs (and DFAs). The ε-closure construction converts any ε-NFA to an equivalent NFA. ε-transitions are a syntactic convenience for Thompson-style constructions.",
                "ce": "ε-NFAs are equivalent to plain NFAs; ε-closure removes ε-transitions without changing the recognized language."
            },
        ],
    },

    # ───────────────────────────── ε-NFA ─────────────────────────────
    "ENFA": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "What is an ε-transition (epsilon-transition)?",
                "c": ["A transition that reads any single symbol", "A transition taken without consuming any input symbol",
                      "A transition that resets the machine to q₀", "A transition only taken on the empty alphabet"],
                "a": 1,
                "e": "An ε-transition is a 'free move' — the machine changes state without reading any input.",
                "ce": "an ε-transition allows the machine to change state without consuming any input symbol."
            },
            {
                "q": "The ε-closure of a state q is defined as...",
                "c": ["The set of states reachable from q using exactly one ε-transition",
                      "The set of all states reachable from q using zero or more ε-transitions",
                      "The set of all accept states reachable from q", "The set {q} alone"],
                "a": 1,
                "e": "ε-CLOSURE(q) is the set of states reachable from q via zero or more ε-transitions (always includes q itself).",
                "ce": "ε-CLOSURE(q) contains all states reachable from q via zero or more ε-transitions, always including q itself."
            },
            {
                "q": "ε-NFAs are equivalent in power to...",
                "c": ["Only Turing machines", "Only pushdown automata",
                      "Both NFAs and DFAs (all recognize regular languages)", "Context-free grammars"],
                "a": 2,
                "e": "ε-NFAs, NFAs, and DFAs all recognize exactly the regular languages — ε-transitions add no extra power.",
                "ce": "ε-NFAs, NFAs, and DFAs all recognize exactly the regular languages; ε-transitions add no extra power."
            },
            {
                "q": "When converting an ε-NFA to a DFA, the DFA's start state is...",
                "c": ["The NFA's start state q₀", "ε-CLOSURE(q₀)",
                      "The set of all accept states", "The empty set ∅"],
                "a": 1,
                "e": "The DFA start state is ε-CLOSURE(q₀) — all states reachable from q₀ for free via ε-transitions.",
                "ce": "the DFA start state is ε-CLOSURE(q₀), all states reachable from q₀ via zero or more ε-transitions."
            },
            {
                "q": "A set S of NFA states is an accept state of the equivalent DFA if...",
                "c": ["S contains every accept state of the NFA", "S contains at least one accept state of the NFA",
                      "S is the ε-closure of an accept state", "S contains only accept states"],
                "a": 1,
                "e": "Any DFA state (subset) that overlaps with F is an accept state — we need at least one NFA accept state in the subset.",
                "ce": "a DFA subset-state S is accepting if S ∩ F ≠ ∅, meaning at least one NFA accept state is in S."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "ε-transitions are most useful for which purpose?",
                "c": ["Speeding up DFA simulation",
                      "Building automata by combining smaller pieces (union, concatenation, star)",
                      "Proving the pumping theorem", "Eliminating dead states"],
                "a": 1,
                "e": "ε-transitions let us 'glue' automata together cleanly — Thompson's construction uses them to build NFA from regex.",
                "ce": "ε-transitions allow composing smaller automata into larger ones for union, concatenation, and Kleene star."
            },
            {
                "q": "In Thompson's construction for r₁ | r₂ (union), ε-transitions connect...",
                "c": ["The accept states of r₁ to the start state of r₂",
                      "A new start state to the start states of r₁ and r₂, and the old accept states to a new accept state",
                      "The start state of r₁ to the accept state of r₂", "Nothing — union requires no ε-transitions"],
                "a": 1,
                "e": "Union in Thompson's construction: new start →ε→ start(r₁), new start →ε→ start(r₂); accept(r₁) →ε→ new accept; accept(r₂) →ε→ new accept.",
                "ce": "union adds a new start with ε-edges to both sub-NFAs' starts, and both sub-NFAs' accepts ε-connect to a new accept."
            },
            {
                "q": "Computing ε-CLOSURE({q}) requires which algorithm?",
                "c": ["Dynamic programming over the grammar",
                      "BFS or DFS graph reachability on ε-transition edges",
                      "The subset construction", "Myhill-Nerode table filling"],
                "a": 1,
                "e": "ε-closure is a reachability problem on the ε-transition graph — BFS/DFS finds all reachable states.",
                "ce": "ε-closure is graph reachability: BFS or DFS on the subgraph of ε-transitions finds all reachable states."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "The state q itself is always _____ in ε-CLOSURE(q).",
                "c": ["Excluded", "Included", "Replaced by its successors", "Optional depending on transitions"],
                "a": 1,
                "e": "ε-CLOSURE includes q itself since zero ε-transitions are allowed — the machine is reachable from q in 0 steps.",
                "ce": "q is always included in ε-CLOSURE(q) because zero ε-transitions are allowed (reflexivity)."
            },
            {
                "q": "In Thompson's construction for r* (Kleene star), ε-transitions from the new accept state go to...",
                "c": ["The new start state only", "The old start state only",
                      "Both the new start state and the old start state", "Nowhere — no outgoing ε-transitions"],
                "a": 0,
                "e": "From the new accept state: →ε→ new start (to loop back). The new start also has →ε→ old start and →ε→ new accept (to allow ε).",
                "ce": "Thompson's r* new-accept state has an ε-edge back to the new start state to enable looping."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "Which regular operation does NOT require ε-transitions in Thompson's construction?",
                "c": ["Union (r₁|r₂)", "Concatenation (r₁r₂)", "Kleene star (r*)", "Single character match (a)"],
                "a": 3,
                "e": "A single character 'a' is just a two-state NFA with one transition — no ε-transitions needed.",
                "ce": "a single character match is just a two-state NFA with one labeled transition; no ε-transitions are needed."
            },
            {
                "q": "After computing ε-closures and applying the subset construction, the resulting DFA recognizes...",
                "c": ["A superset of the original ε-NFA's language", "A subset of the original language",
                      "Exactly the same language as the original ε-NFA", "Only strings with no ε-transitions used"],
                "a": 2,
                "e": "The subset construction with ε-closures produces a DFA equivalent to the ε-NFA — same language recognized.",
                "ce": "the ε-closure-augmented subset construction produces a DFA recognizing exactly the same language as the ε-NFA."
            },
            {
                "q": "Thompson's construction converts a regular expression of size n (number of symbols/operators) to an ε-NFA with at most how many states?",
                "c": ["n states", "2n states", "n² states", "2^n states"],
                "a": 1,
                "e": "Thompson's construction adds at most 2 states per regex operator/symbol — an expression of size n yields at most 2n states.",
                "ce": "Thompson's construction adds at most 2 states per regex symbol or operator, giving at most 2n states total."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "Why don't ε-transitions add extra power beyond NFA/DFA?",
                "c": ["They can only be used once per string",
                      "Any ε-transition can be 'collapsed' by computing ε-closures, reducing to an equivalent NFA without ε-transitions",
                      "ε-transitions always lead to dead states",
                      "The alphabet Σ does not include ε"],
                "a": 1,
                "e": "ε-transitions are syntactic sugar — computing ε-closures bakes the free moves into regular transitions, giving an equivalent NFA.",
                "ce": "ε-transitions can be removed by computing ε-closures, producing an equivalent NFA without adding power."
            },
            {
                "q": "In converting an ε-NFA to an equivalent NFA (removing ε-transitions), the new transition function δ'(q, a) is defined as...",
                "c": ["δ(q, a)", "ε-CLOSURE(δ(q, a))",
                      "⋃_{p ∈ ε-CLOSURE(q)} ε-CLOSURE(δ(p, a))", "δ(ε-CLOSURE(q), a)"],
                "a": 2,
                "e": "For each state in ε-CLOSURE(q), compute δ on symbol a, then take ε-closure of all results: δ'(q,a) = ⋃_{p∈ε-CLOSURE(q)} ε-CLOSURE(δ(p,a)).",
                "ce": "from each state in ε-CLOSURE(q), follow δ on a, then take ε-closure of all results."
            },
            {
                "q": "In Thompson's construction for concatenation r₁r₂, the start state of the combined NFA is...",
                "c": ["A new state with ε-transitions to the starts of both r₁ and r₂",
                      "The start state of r₁, with ε-transitions from r₁'s accept states to r₂'s start state",
                      "The start state of r₂",
                      "A merged state of r₁'s start and r₂'s start"],
                "a": 1,
                "e": "Concatenation: the combined NFA starts at r₁'s start state; ε-transitions from r₁'s (now non-accepting) accept states lead to r₂'s start.",
                "ce": "concatenation uses r₁'s start as the combined start; ε-transitions from r₁'s accepts lead to r₂'s start."
            },
            {
                "q": "When computing the DFA transition δ_DFA(S, a) from a set S of ε-NFA states on input a, the result is...",
                "c": ["δ_NFA(S, a) directly",
                      "ε-CLOSURE(⋃_{q∈S} δ_NFA(q, a))",
                      "⋃_{q∈ε-CLOSURE(S)} δ_NFA(q, a)",
                      "ε-CLOSURE(S) ∪ δ_NFA(S, a)"],
                "a": 1,
                "e": "Collect all states reachable from S via δ_NFA on a, then take the ε-closure of the result: ε-CLOSURE(⋃_{q∈S} δ_NFA(q, a)).",
                "ce": "from set S on symbol a: union all a-transitions from states in S, then take ε-closure of the result."
            },
            {
                "q": "A subset S (in the ε-NFA→DFA construction) is designated an accept state if and only if...",
                "c": ["S equals F exactly",
                      "S ∩ F ≠ ∅ (S contains at least one accept state of the ε-NFA)",
                      "ε-CLOSURE(S) ⊆ F",
                      "S is the ε-closure of an accept state only"],
                "a": 1,
                "e": "A DFA subset-state S is accepting whenever it contains at least one original accept state — S ∩ F ≠ ∅.",
                "ce": "subset S is an accept state if S ∩ F ≠ ∅, i.e., at least one ε-NFA accept state is in S."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "The ε-closure of a state q in an ε-NFA is...",
                "c": ["The set of states reachable from q on exactly one ε-transition",
                      "The set of all states reachable from q by zero or more ε-transitions (including q itself)",
                      "The complement of q's reachable states",
                      "Only the states directly adjacent to q"],
                "a": 1,
                "e": "ε-closure(q) = {r | r is reachable from q via zero or more ε-transitions}. Always contains q itself (zero transitions). BFS/DFS computes it in O(|Q|·|δ_ε|).",
                "ce": "ε-closure(q) is all states reachable from q via zero or more ε-transitions, including q itself."
            },
            {
                "q": "In the ε-NFA to DFA conversion, the DFA transition δ'(S, a) equals...",
                "c": ["∪_{q∈S} δ(q, a)",
                      "ε-closure(∪_{q∈S} δ(q, a)) — union of transitions on 'a' from all states in S, then take ε-closure",
                      "∩_{q∈S} ε-closure(δ(q, a))",
                      "ε-closure(S) ∪ δ(q₀, a)"],
                "a": 1,
                "e": "DFA transition: from subset S on symbol a, move to ∪_{q∈S} δ(q,a), then take ε-closure. DFA start = ε-closure(q₀); accept states = subsets containing any NFA accept state.",
                "ce": "δ'(S, a) = ε-closure(∪_{q∈S} δ(q, a)): union all a-transitions from S, then take ε-closure."
            },
            {
                "q": "Kleene's theorem (regex → NFA direction) uses Thompson's construction, which works by...",
                "c": ["Direct construction of a DFA by induction on regex structure",
                      "Structural induction on regex, building ε-NFA fragments composed via ε-transitions for union, concatenation, and Kleene star",
                      "Applying the pumping lemma to every regex",
                      "Using the Myhill-Nerode theorem to bound state count"],
                "a": 1,
                "e": "Thompson's construction: base cases for ε, ∅, and single symbols; inductive cases use ε-transitions to compose NFAs for r|s, rs, and r*. Each fragment has exactly one accept state.",
                "ce": "Thompson's construction uses structural induction, building ε-NFA fragments composed via ε-transitions for union, concatenation, and Kleene star."
            },
            {
                "q": "ε-transitions in ε-NFAs are primarily useful because...",
                "c": ["They allow the automaton to accept ε in every language",
                      "They simplify building automata for union (r|s), concatenation (rs), and Kleene star (r*) — making Thompson's construction elegant",
                      "They reduce the total number of states vs DFAs",
                      "They allow the automaton to 'look ahead' in the input"],
                "a": 1,
                "e": "ε-transitions enable clean composition: for r|s add a start with ε-edges to both sub-NFAs; for rs connect r's accept to s's start via ε; for r* add a loop-back ε-edge.",
                "ce": "ε-transitions simplify building automata for union, concatenation, and Kleene star in Thompson's construction."
            },
            {
                "q": "A string w = a₁a₂...aₙ is accepted by an ε-NFA M if...",
                "c": ["M spells out w in exactly n transitions with no ε-transitions",
                      "There exists a sequence r₀, r₁, ..., rₙ where r₀ ∈ ε-closure(q₀), each rᵢ ∈ ε-closure(δ(rᵢ₋₁, aᵢ)), and rₙ ∈ F",
                      "The DFA converted from M accepts w",
                      "All states reachable on w are accepting"],
                "a": 1,
                "e": "ε-NFA acceptance: start in ε-closure(q₀); after each symbol aᵢ take ε-closure of all states reachable on aᵢ. Accept if the final set intersects F.",
                "ce": "acceptance requires a sequence where r₀ ∈ ε-closure(q₀), each rᵢ ∈ ε-closure(δ(rᵢ₋₁, aᵢ)), and rₙ ∈ F."
            },
            {
                "q": "An ε-NFA with multiple start states {q₁, q₂, ..., q_k} can be converted to one with a single start state by...",
                "c": ["Picking the state with the most transitions as the sole start",
                      "Adding a new start state q₀ with ε-transitions to each qᵢ (does not change the accepted language)",
                      "Merging all start states into one, combining their transitions",
                      "Impossible — multiple start states cannot be consolidated"],
                "a": 1,
                "e": "Add fresh q₀ with ε-transitions to every original start state. ε-closure(q₀) = {q₀} ∪ ε-closure(q₁) ∪ ... ∪ ε-closure(q_k), exactly replicating the original behavior.",
                "ce": "add a fresh q₀ with ε-transitions to each original start state; ε-closure(q₀) covers all original starts."
            },
        ],
    },

    # ───────────────────────────── REGEX ─────────────────────────────
    "REGEX": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "The union operation r₁|r₂ in a regular expression means...",
                "c": ["A string is in both L(r₁) and L(r₂)", "A string is in L(r₁) OR L(r₂) (or both)",
                      "r₁ is concatenated with r₂", "r₁ and r₂ are the same language"],
                "a": 1,
                "e": "Union (|) means set union: L(r₁|r₂) = L(r₁) ∪ L(r₂).",
                "ce": "union (|) means a string is in L(r₁) OR L(r₂) (or both); L(r₁|r₂) = L(r₁) ∪ L(r₂)."
            },
            {
                "q": "The regular expression ∅ denotes...",
                "c": ["The empty string ε", "The empty language (no strings accepted)",
                      "A wildcard matching any character", "The string '∅'"],
                "a": 1,
                "e": "∅ is the empty language — no string is in L(∅). It is different from ε, which is the empty-string language {ε}.",
                "ce": "∅ is the empty language; L(∅) = {} — no string is accepted."
            },
            {
                "q": "The regular expression ε denotes...",
                "c": ["The empty language ∅", "The language containing only the empty string {ε}",
                      "Any single character", "All strings over Σ"],
                "a": 1,
                "e": "ε denotes the language {ε} — only the empty string. Don't confuse with ∅ (no strings at all).",
                "ce": "ε denotes the language {ε}: exactly one string, the empty string."
            },
            {
                "q": "The Kleene star r* means...",
                "c": ["Exactly one occurrence of r", "One or more occurrences of r",
                      "Zero or more concatenations of strings from L(r)", "The complement of L(r)"],
                "a": 2,
                "e": "r* = {ε} ∪ L(r) ∪ L(r)L(r) ∪ ... — zero or more repetitions (always includes ε).",
                "ce": "r* = zero or more concatenations of strings from L(r); it always includes ε."
            },
            {
                "q": "Kleene's theorem states that...",
                "c": ["Every language can be described by a regex",
                      "Regular expressions and finite automata describe exactly the same class of languages",
                      "Every NFA can be converted to a regex in linear time",
                      "Regex can describe context-free languages"],
                "a": 1,
                "e": "Kleene's theorem: regex ↔ DFA/NFA — they all describe exactly the regular languages.",
                "ce": "Kleene's theorem: regular expressions and finite automata describe exactly the same class of languages."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "The expression r+ is shorthand for...",
                "c": ["r* (Kleene star)", "r | ε", "rr* (one or more occurrences of r)", "r∅"],
                "a": 2,
                "e": "r+ = rr* — one or more occurrences. Unlike r*, it does NOT include the empty string (unless ε ∈ L(r)).",
                "ce": "r+ = rr* means one or more occurrences of r; ε is included only if r itself accepts ε."
            },
            {
                "q": "Which is NOT a primitive operation in the formal definition of regular expressions?",
                "c": ["Union (|)", "Concatenation (·)", "Kleene star (*)", "Intersection (∩)"],
                "a": 3,
                "e": "The three primitive regex operations are union, concatenation, and Kleene star. Intersection is not primitive (though regular languages are closed under it).",
                "ce": "intersection (∩) is NOT a primitive regex operation; the three primitives are union, concatenation, and Kleene star."
            },
            {
                "q": "The GNFA (Generalized NFA) method converts a DFA to a regular expression by...",
                "c": ["Adding ε-transitions to every pair of states",
                      "Eliminating states one at a time, updating edge labels with regex expressions",
                      "Reversing all transitions and running the subset construction",
                      "Applying the pumping lemma repeatedly"],
                "a": 1,
                "e": "State elimination: add new start/accept states with ε edges, then remove intermediate states and update regex labels on remaining edges.",
                "ce": "the GNFA method adds new start/accept states, then removes intermediate states one by one, updating edge labels with regex expressions."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "The language {w | w contains the substring 'ab'} is expressed as...",
                "c": ["ab", "(a|b)*ab", "(a|b)*ab(a|b)*", "a*b*"],
                "a": 2,
                "e": "(a|b)* matches any prefix, ab matches the required substring, (a|b)* matches any suffix.",
                "ce": "(a|b)*ab(a|b)* matches any string with 'ab' as a substring (anything before, ab, anything after)."
            },
            {
                "q": "What is the language of the regex (ab)*?",
                "c": ["{ab}", "{a, b, ab}", "{ε, ab, aabb, ...}", "{ε, ab, abab, ababab, ...}"],
                "a": 3,
                "e": "(ab)* = zero or more copies of 'ab': ε, ab, abab, ababab, ... Note that aabb is NOT in this language.",
                "ce": "(ab)* = {ε, ab, abab, ababab, ...}: zero or more copies of the string 'ab' concatenated."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "r? (r-optional) is shorthand for...",
                "c": ["r*", "r+", "r | ε (zero or one occurrence of r)", "rr"],
                "a": 2,
                "e": "r? = r | ε — zero or one occurrence of r (used in many programming regex engines).",
                "ce": "r? means r | ε: exactly zero or one occurrence of r."
            },
            {
                "q": "Regular expressions can describe exactly...",
                "c": ["All languages", "Context-free languages", "Regular languages", "Only finite languages"],
                "a": 2,
                "e": "By Kleene's theorem, regular expressions describe exactly the regular languages — same as DFAs and NFAs.",
                "ce": "By Kleene's theorem, regular expressions describe exactly the regular languages — the same class recognized by DFAs and NFAs."
            },
            {
                "q": "To convert a DFA with n states to a regular expression using GNFA state elimination, the GNFA initially has how many states?",
                "c": ["n", "n − 1", "n + 1", "n + 2"],
                "a": 3,
                "e": "The GNFA adds a new start state and a new unique accept state to the DFA, giving n + 2 states total before elimination begins.",
                "ce": "The GNFA starts with n + 2 states: the original n DFA states plus a new start and a new unique accept state."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "Which language CANNOT be described by any regular expression?",
                "c": ["{w | w has odd length}", "{aⁿbⁿ | n ≥ 1}",
                      "{w | w starts with 'aa'}", "{w | w contains at least two b's}"],
                "a": 1,
                "e": "{aⁿbⁿ} requires counting — matching n a's with n b's. This is beyond the power of regular expressions (it's context-free).",
                "ce": "{aⁿbⁿ} requires matching equal counts of a's and b's — this is context-free, not regular, so no regex exists for it."
            },
            {
                "q": "The expression (a|ε)(b|ε) matches exactly which set of strings?",
                "c": ["{ab}", "{a, b, ab}", "{ε, a, b, ab}", "{ε, ab}"],
                "a": 2,
                "e": "(a|ε) contributes ε or a; (b|ε) contributes ε or b. Combining: ε·ε=ε, ε·b=b, a·ε=a, a·b=ab → {ε, a, b, ab}.",
                "ce": "(a|ε)(b|ε) concatenates zero-or-one a with zero-or-one b, yielding exactly {ε, a, b, ab}."
            },
            {
                "q": "After GNFA state elimination reduces a DFA (with n+2 GNFA states) to a regex, how many states remain in the final GNFA?",
                "c": ["0 — all states are removed", "1 — only the accept state remains",
                      "2 — only the special start and accept states remain, connected by the final regex",
                      "n — all original DFA states minus one"],
                "a": 2,
                "e": "State elimination removes all n intermediate states one by one, leaving exactly 2 states (new start and new accept) connected by one edge labeled with the final regex.",
                "ce": "After eliminating all n intermediate states, exactly 2 states remain — the new start and new accept — connected by a single edge whose label is the final regex."
            },
            {
                "q": "Arden's Lemma: if X = AX | B (where A does not contain ε), the unique solution for X is...",
                "c": ["X = A*B | B", "X = A*B", "X = AB*", "X = (A | B)*"],
                "a": 1,
                "e": "Arden's Lemma: X = AX | B has unique solution X = A*B. It is used to solve systems of linear regex equations when deriving a regex from a DFA.",
                "ce": "Arden's Lemma: when ε ∉ A, X = AX | B has the unique solution X = A*B."
            },
            {
                "q": "What strings does the regex (0|1)*1(0|1)² describe?",
                "c": ["All binary strings ending in exactly '100' or '110'",
                      "All binary strings where the 3rd-from-last character is 1",
                      "All binary strings of even length containing at least one 1",
                      "All binary strings of length exactly 3"],
                "a": 1,
                "e": "(0|1)* is any prefix, then '1', then exactly two more characters (0|1)² — together this captures any string where position |w|-2 is '1', i.e., the 3rd-from-last character.",
                "ce": "(0|1)*1(0|1)² matches any binary string where the 3rd-from-last character is 1, since the 1 is followed by exactly two more characters."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "The state elimination method for converting a DFA to a regular expression works by...",
                "c": ["Guessing a regex and verifying it matches the DFA",
                      "Iteratively removing non-start, non-accept states and updating edge labels with union/concatenation until only start and accept remain",
                      "Running the DFA on all strings up to length |Q| and building a regex from results",
                      "Using Myhill-Nerode to read off the regex directly"],
                "a": 1,
                "e": "State elimination (GNFA method): rip out each intermediate state q; for each path i→q→j, add R(i,q)·R(q,q)*·R(q,j) to edge i→j. After eliminating all intermediate states, the remaining edge label is the regex.",
                "ce": "GNFA state elimination: for each removed state q and each pair (i, j), update the i→j edge label to include R(i,q)·R(q,q)*·R(q,j); the final two-state label is the regex."
            },
            {
                "q": "Which of these is NOT a valid algebraic identity for regular expressions?",
                "c": ["r + s = s + r  (commutativity of union)",
                      "(rs)t = r(st)  (associativity of concatenation)",
                      "r·s = s·r  (commutativity of concatenation)",
                      "r* = ε + r·r*  (unfolding of Kleene star)"],
                "a": 2,
                "e": "Concatenation is NOT commutative: 'ab' ≠ 'ba' in general. Union is commutative, concatenation is associative, and unfolding r* = ε + rr* is always valid.",
                "ce": "Concatenation is NOT commutative in general — the strings 'ab' and 'ba' are different, so r·s ≠ s·r."
            },
            {
                "q": "Regular expressions cannot directly express complement or intersection, yet these operations preserve regularity. Why?",
                "c": ["Complement and intersection are not effective operations on strings",
                      "Regex = DFA in power; DFAs are closed under complement/intersection via product/complement construction, so the result IS regular — just not expressed by a single regex formula",
                      "Complement and intersection always produce non-regular languages",
                      "These operations require pushdown automata"],
                "a": 1,
                "e": "Convert regex→DFA, apply the DFA operation, then convert back to regex. The language is regular; the regex exists. The standard regex operators just don't include a direct complement/intersection syntax.",
                "ce": "Regex = DFA in power; DFA operations (complement/intersection) always produce regular languages, so the result is regular — it just can't be expressed by a single regex formula directly."
            },
            {
                "q": "There exist languages where the smallest regex is exponentially larger than the minimal DFA. This illustrates that...",
                "c": ["Regular expressions are less powerful than DFAs",
                      "Regular expressions and DFAs can have very different descriptional complexities for the same language",
                      "DFAs always require fewer symbols than regular expressions",
                      "Regular expressions cannot represent all regular languages"],
                "a": 1,
                "e": "Descriptional complexity: languages exist where minimal DFAs have O(n) states but equivalent regexes require Ω(2^n) symbols, and vice versa. Same expressive power, different conciseness.",
                "ce": "Regular expressions and DFAs have the same expressive power but can differ exponentially in descriptional complexity — the same language may need far more symbols in one form than the other."
            },
            {
                "q": "The language {ww | w ∈ {a,b}*} (a string repeated twice) is...",
                "c": ["Regular — expressible as (a|b)*(a|b)*",
                      "Context-free but not regular — no finite automaton can remember the first half to compare with the second",
                      "Context-sensitive but not context-free",
                      "Decidable only by a Turing machine"],
                "a": 1,
                "e": "{ww} is not regular (Pumping Lemma) and not context-free (CFL Pumping Lemma). It is context-sensitive. No finite-memory device can match both halves.",
                "ce": "{ww} is context-sensitive but not context-free — it cannot be recognized by any PDA because matching both halves requires remembering the entire first half."
            },
            {
                "q": "A 'star-free' regular expression uses union, concatenation, and complement but NOT Kleene star. Star-free expressions define exactly...",
                "c": ["All regular languages",
                      "Only finite languages",
                      "The aperiodic (counter-free) regular languages — whose minimal DFA has no nontrivial cycles",
                      "Context-free languages only"],
                "a": 2,
                "e": "Schützenberger's theorem (1965): a regular language is star-free iff its syntactic monoid is aperiodic. Star-free = languages definable in first-order logic over string order. E.g., (ab)* requires counting mod 2 and is not star-free.",
                "ce": "Star-free expressions (union, concatenation, complement — no Kleene star) define exactly the aperiodic regular languages, whose minimal DFAs have no nontrivial cycles."
            },
        ],
    },

    # ───────────────────────────── PUMPING THEOREM ─────────────────────────────
    "PUMP": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "The Pumping Theorem (for regular languages) is used to prove...",
                "c": ["A language IS regular", "A language is NOT regular",
                      "A DFA is minimal", "An NFA can be converted to a DFA"],
                "a": 1,
                "e": "The pumping lemma is a proof tool for non-regularity — it gives a necessary condition that every regular language must satisfy.",
                "ce": "The pumping lemma gives a necessary condition that all regular languages satisfy; failing it proves a language is NOT regular."
            },
            {
                "q": "If L is regular with pumping length p, then any string s ∈ L with |s| ≥ p can be written as s = xyz where which conditions hold?",
                "c": ["|x| ≥ 1, |y| ≥ 1, xy^i z ∈ L for all i ≥ 0",
                      "|xy| ≤ p, |y| ≥ 1, xy^i z ∈ L for all i ≥ 0",
                      "|xy| ≥ p, |z| ≥ 1, xy^i z ∈ L for all i ≥ 1",
                      "|x| = |z|, |y| ≥ 1, xy^i z ∈ L for some i ≥ 0"],
                "a": 1,
                "e": "The three conditions: (1) |xy| ≤ p, (2) |y| ≥ 1 (y is non-empty), (3) xy^i z ∈ L for ALL i ≥ 0.",
                "ce": "The three conditions are: |xy| ≤ p (pump within first p chars), |y| ≥ 1 (y is non-empty so pumping changes the string), and xy^i z ∈ L for ALL i ≥ 0."
            },
            {
                "q": "The condition |y| ≥ 1 in the pumping theorem ensures...",
                "c": ["The string s has at least one character",
                      "The pumpable portion y is non-empty (so pumping actually changes the string)",
                      "The machine has at least one accept state", "The DFA has at least p states"],
                "a": 1,
                "e": "If y=ε, pumping (repeating y) changes nothing — the condition |y|≥1 ensures pumping actually produces new strings.",
                "ce": "|y| ≥ 1 guarantees y is non-empty, so pumping (repeating or removing y) actually changes the string length and can produce a contradiction."
            },
            {
                "q": "The condition |xy| ≤ p ensures...",
                "c": ["The string s has exactly p characters", "The pumpable portion y occurs within the first p characters of s",
                      "x and y together have more than p characters", "The DFA always accepts xy"],
                "a": 1,
                "e": "|xy|≤p ensures y lies within the first p characters — this is where the DFA must repeat a state (by pigeonhole), so that portion can be pumped.",
                "ce": "|xy| ≤ p forces the pumpable portion y to lie within the first p characters, where a state repetition must occur by the pigeonhole principle."
            },
            {
                "q": "In a pumping theorem proof, who 'chooses' the pumping length p?",
                "c": ["We (the prover) choose p to make our string work",
                      "The adversary (the proof assumes L is regular, so p is given to us by that assumption)",
                      "Both sides negotiate p", "p is always equal to the number of states in the DFA"],
                "a": 1,
                "e": "p is given by the assumption that L is regular. We must work for ANY p — we cannot choose it ourselves.",
                "ce": "p is given to us by the assumption that L is regular — we do not get to pick it; we must handle any p the adversary provides."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "In a pumping theorem proof, who chooses the string s?",
                "c": ["The adversary (we must handle any string)", "We (the prover) choose a specific s ∈ L with |s| ≥ p",
                      "p determines s automatically", "s must be the shortest string in L"],
                "a": 1,
                "e": "We strategically choose s ∈ L with |s|≥p. We should pick s so that any valid decomposition xyz leads to a contradiction.",
                "ce": "We (the prover) choose the string s ∈ L with |s| ≥ p, picking it strategically so that any valid xyz decomposition can be pumped to a contradiction."
            },
            {
                "q": "In a pumping theorem proof, who chooses the decomposition xyz?",
                "c": ["We (the prover) choose the best decomposition for us",
                      "The adversary — we must show ALL valid decompositions lead to contradiction",
                      "It is fixed by the theorem", "Both sides choose simultaneously"],
                "a": 1,
                "e": "The adversary picks the decomposition (within the constraints). Our proof must work for every valid xyz split.",
                "ce": "The adversary chooses the decomposition xyz (within the constraints |xy|≤p and |y|≥1); our proof must derive a contradiction for every valid split they could pick."
            },
            {
                "q": "In a pumping theorem proof, who chooses the pump value i?",
                "c": ["The adversary (they try to break our argument)",
                      "We (the prover) — we pick i ≥ 0 to produce a string not in L",
                      "i is always 0 or 2", "i must be greater than p"],
                "a": 1,
                "e": "We pick i to generate the contradiction — usually i=0 (delete y) or i=2 (duplicate y) is enough.",
                "ce": "We (the prover) choose the pump value i ≥ 0 to produce a string xy^iz not in L — usually i=0 (remove y) or i=2 (add one extra copy of y) suffices."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "The pumping theorem is a _____ condition for regularity.",
                "c": ["Sufficient (passing it proves regularity)", "Necessary (if regular, must satisfy it; failing it proves non-regularity)",
                      "Both necessary and sufficient", "Neither necessary nor sufficient"],
                "a": 1,
                "e": "It's necessary: every regular language satisfies it. But it's not sufficient — some non-regular languages also satisfy it.",
                "ce": "The pumping theorem is necessary but not sufficient — every regular language satisfies it, but some non-regular languages also satisfy it, so passing it does not prove regularity."
            },
            {
                "q": "If a language L fails the pumping theorem test, we can conclude...",
                "c": ["L might still be regular", "L is definitely NOT regular",
                      "L is context-free", "L is undecidable"],
                "a": 1,
                "e": "Failing the pumping lemma (finding a string that cannot be pumped) is a proof that L is not regular.",
                "ce": "Failing the pumping lemma — finding a string in L that violates the pumping conditions for every valid decomposition — definitively proves L is not regular."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "If a language L passes the pumping theorem test, we can conclude...",
                "c": ["L is regular", "L is context-free",
                      "Nothing definitive about regularity — passing is inconclusive", "L is decidable"],
                "a": 2,
                "e": "Passing the pumping lemma is inconclusive — some non-regular languages also satisfy the pumping lemma. You need Myhill-Nerode to prove regularity.",
                "ce": "Passing the pumping lemma is inconclusive — non-regular languages can also satisfy it, so it cannot be used to prove regularity."
            },
            {
                "q": "The key intuition behind the pumping theorem is based on...",
                "c": ["The Church-Turing thesis", "The pigeonhole principle — a DFA with p states must repeat a state when reading any string of length ≥ p",
                      "Cantor's diagonalization", "Rice's theorem"],
                "a": 1,
                "e": "A DFA with p states reading a string of length ≥ p must visit p+1 states — by pigeonhole, some state repeats, creating a pumpable loop.",
                "ce": "The pumping theorem is grounded in the pigeonhole principle: a DFA with p states reading ≥ p symbols must revisit a state, creating a repeatable (pumpable) loop."
            },
            {
                "q": "To prove {a^p | p is prime} is not regular, we choose s = a^m where m is prime and m ≥ p. For any decomposition xyz with |y|=k≥1, to get a contradiction we need a pump value i such that |xy^i z| is composite. What strategy works?",
                "c": ["Set i = 0; |xz| = m − k, which is always composite",
                      "Choose i so that m + (i−1)k is composite (e.g., i = m/k + 1 gives a composite length)",
                      "All primes satisfy the pumping lemma, so no contradiction is possible",
                      "We need to use the Myhill-Nerode theorem instead"],
                "a": 1,
                "e": "By choosing i = m/k + 1 (or a similar composite-producing value), the pumped string has composite length, so it's not in the prime-lengths language.",
                "ce": "Choose i so that m + (i−1)k is composite — e.g., i = m/k + 1 produces a length divisible by m/k, which is composite for large enough m."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "The correct order of moves in the pumping theorem 'game' is...",
                "c": ["We pick s → Adversary picks p → We pick xyz → Adversary picks i",
                      "Adversary picks p → We pick s ∈ L with |s|≥p → Adversary picks xyz → We pick i to get contradiction",
                      "We pick p and s → Adversary picks xyz and i",
                      "Adversary picks p and xyz → We pick s and i"],
                "a": 1,
                "e": "The game: Adversary picks p → We pick s → Adversary picks decomposition xyz → We pick i. Our job is to always find a winning i.",
                "ce": "The correct order is: adversary picks p → we pick s ∈ L with |s|≥p → adversary picks xyz decomposition → we pick i to reach a contradiction."
            },
            {
                "q": "The Myhill-Nerode theorem is a stronger tool than the pumping theorem because...",
                "c": ["It is easier to apply", "It is both necessary and sufficient for regularity, while the pumping theorem is only necessary",
                      "It works on context-free languages too", "It gives the pumping length directly"],
                "a": 1,
                "e": "Myhill-Nerode: L is regular iff the number of equivalence classes of ≡_L is finite. It gives an exact characterization, not just a one-sided test.",
                "ce": "Myhill-Nerode is both necessary AND sufficient for regularity — it gives a complete characterization, unlike the pumping lemma which is only one-sided."
            },
            {
                "q": "To prove {a^n b^n | n ≥ 0} is not regular, the best choice of s is...",
                "c": ["s = a^p (only a's, length p)",
                      "s = a^p b^p (equal counts, length 2p ≥ p)",
                      "s = ab (the shortest member, length 2)",
                      "s = a^p b (only one b)"],
                "a": 1,
                "e": "s = a^p b^p has length 2p ≥ p, so it satisfies |s|≥p. Since |xy|≤p, y consists only of a's — pumping up (i=2) gives a^(p+k)b^p ∉ L.",
                "ce": "Choose s = a^p b^p: since |xy| ≤ p, y falls within the a^p prefix (only a's), so pumping gives a^(p+k)b^p with unequal counts, contradicting membership in {a^n b^n}."
            },
            {
                "q": "The pumping lemma for context-free languages decomposes a string s as uvxyz where the conditions include...",
                "c": ["|vxy| ≤ p, |vy| ≥ 1, and uv^i xy^i z ∈ L for all i ≥ 0",
                      "|vxy| ≥ p, |vy| ≥ 1, and uv^i xy^i z ∈ L for some i",
                      "|uvx| ≤ p, |vy| ≥ 1, and uv^i xy^i z ∈ L for all i ≥ 0",
                      "|vxy| ≤ p, |vy| = 0, and uv^i xy^i z ∈ L for all i ≥ 0"],
                "a": 0,
                "e": "CFL pumping lemma: s = uvxyz with |vxy|≤p, |vy|≥1, and uv^i xy^i z ∈ L for ALL i≥0. The middle segment vxy is bounded and vy is non-empty.",
                "ce": "The CFL pumping lemma conditions are: |vxy| ≤ p (bounded middle), |vy| ≥ 1 (non-empty pump), and uv^i xy^i z ∈ L for all i ≥ 0."
            },
            {
                "q": "When using s = a^p b^p in the pumping theorem for {a^n b^n}, the constraint |xy| ≤ p forces y to consist of...",
                "c": ["b's only",
                      "Both a's and b's (a mix)",
                      "a's only",
                      "Either a's only or b's only depending on x"],
                "a": 2,
                "e": "|xy| ≤ p and s = a^p b^p, so xy lies entirely in the first p characters (all a's). Therefore y is a non-empty run of a's only.",
                "ce": "With s = a^p b^p and |xy| ≤ p, the xy portion lies entirely within the first p characters (all a's), so y must consist only of a's."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "To prove L = {0ⁿ1ⁿ2ⁿ | n ≥ 0} is not regular with the Pumping Lemma, the best string choice is...",
                "c": ["s = 0^p (all zeros)",
                      "s = 0^p 1^p 2^p (length 3p ≥ p) — the pumped portion xy lies in 0^p, so pumping changes the 0-count while 1s and 2s stay at p",
                      "s = (012)^p",
                      "s = 0^p 1 (deliberately unequal)"],
                "a": 1,
                "e": "Choose s = 0^p 1^p 2^p. |xy| ≤ p forces xy entirely within 0^p. Pumping gives 0^(p+k)1^p2^p for k ≥ 1 — unequal counts, contradicting membership. (Note: {0ⁿ1ⁿ2ⁿ} is also non-CFL.)",
                "ce": "Choose s = 0^p 1^p 2^p: |xy| ≤ p forces y inside the 0^p block, so pumping gives unequal counts of 0s, 1s, and 2s — a contradiction."
            },
            {
                "q": "The Pumping Lemma for CFLs: any s ∈ L with |s| ≥ p can be written s = uvwxy where...",
                "c": ["|vwx| ≤ p, |vx| ≥ 1, and for all i ≥ 0, uvᵢwxᵢy ∈ L (v and x pump together)",
                      "|vwx| ≤ p, |v| ≥ 1, and for all i ≥ 0, uvᵢwxy ∈ L (only v pumps)",
                      "|uvw| ≤ p and for all i ≥ 0, uᵢvwxyᵢ ∈ L",
                      "|vx| ≤ p and v, x pump independently"],
                "a": 0,
                "e": "CFL Pumping Lemma: s=uvwxy with |vwx|≤p, |vx|≥1, uvᵢwxᵢy∈L for all i≥0. Both v and x pump together. The |vwx|≤p constraint comes from the parse tree height bound via pigeonhole.",
                "ce": "CFL pumping lemma: s = uvwxy with |vwx| ≤ p, |vx| ≥ 1, and uv^i wx^i y ∈ L for all i ≥ 0 — both v and x must pump together."
            },
            {
                "q": "To show L = {a^(n²) | n ≥ 0} is not regular, which argument correctly applies the Pumping Lemma?",
                "c": ["Choose s = a^(p²). Any decomposition with |y|=k≥1 gives a^(p²+k). But (p+1)² = p²+2p+1 > p²+k for k≤p, so p²+k is not a perfect square. Contradiction.",
                      "Choose s = a^p. Then xyyz = a^(p+k), which is a perfect square for some k — no contradiction.",
                      "L is regular because all strings are over a unary alphabet.",
                      "The Pumping Lemma cannot be applied to unary languages."],
                "a": 0,
                "e": "s = a^(p²): after pumping, get a^(p²+k) for 1≤k≤p. Gap between p² and (p+1)² is 2p+1 > p ≥ k, so p²+k strictly falls between consecutive perfect squares. Not in L. Contradiction.",
                "ce": "Choose s = a^(p²): pumping gives a^(p²+k) for 1 ≤ k ≤ p; since the gap between p² and (p+1)² is 2p+1 > k, the pumped length is not a perfect square — contradiction."
            },
            {
                "q": "An alternative to the Pumping Lemma for proving non-regularity is using closure properties. This approach works by...",
                "c": ["The Myhill-Nerode method",
                      "Assuming L is regular, applying a closure operation (e.g. intersection with a regular language or homomorphism) to derive a known non-regular language — a contradiction",
                      "The diagonal argument",
                      "The state-minimization argument"],
                "a": 1,
                "e": "Closure-property arguments: if L were regular and R is regular, then L ∩ R is regular. If L ∩ R equals a known non-regular language, we have a contradiction. Often simpler than the Pumping Lemma for certain languages.",
                "ce": "Closure-property proofs: assume L is regular, intersect with a regular language R, and show L ∩ R equals a known non-regular language — a contradiction proving L is not regular."
            },
            {
                "q": "A language L satisfies the conclusion of the Pumping Lemma yet is NOT regular. This is possible because...",
                "c": ["The Pumping Lemma is an incorrect theorem",
                      "The Pumping Lemma gives a necessary but NOT sufficient condition for regularity — satisfying it doesn't prove regularity",
                      "Every language satisfies the Pumping Lemma",
                      "The Pumping Lemma only applies to finite languages"],
                "a": 1,
                "e": "The Pumping Lemma is necessary (regular ⇒ pumpable) but not sufficient. Non-regular languages can satisfy the pumping property. The Myhill-Nerode theorem gives an iff characterization.",
                "ce": "The pumping lemma is necessary but not sufficient — some non-regular languages also satisfy it, so a language can pass the pumping test and still be non-regular."
            },
            {
                "q": "Ogden's Lemma extends the CFL Pumping Lemma by allowing us to 'mark' symbols. Its advantage is...",
                "c": ["It proves more languages are context-free",
                      "It gives stronger control over where the pumped portion vx falls, enabling proofs where the standard CFL lemma's pump dodges the critical structure",
                      "It eliminates the |vwx| length constraint",
                      "It converts any CFL proof into a regular language proof"],
                "a": 1,
                "e": "Ogden's Lemma: mark p symbols; then vwx must contain a marked symbol and |vx|≥1. This forces the pump into a chosen region — useful when the standard lemma can't pin down the pump location.",
                "ce": "Ogden's Lemma strengthens the CFL pumping lemma by allowing you to mark positions, forcing the pump (v and x) to fall in a specific region of the string."
            },
        ],
    },

    # ───────────────────────────── CFG ─────────────────────────────
    "CFG": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "A CFG is formally defined as a 4-tuple. Which option is correct?",
                "c": ["(Q, Σ, δ, q₀)", "(V, Σ, R, S)", "(V, T, P, q₀, F)", "(Q, Σ, γ, S)"],
                "a": 1,
                "e": "A CFG is (V, Σ, R, S): Variables (non-terminals), Terminal alphabet, Production Rules, Start variable.",
                "ce": "A CFG is the 4-tuple (V, Σ, R, S): variables (non-terminals), terminal alphabet, production rules, and start variable."
            },
            {
                "q": "A production rule in a CFG has the form...",
                "c": ["a → A (terminal rewrites to variable)", "A → α (variable rewrites to string of variables and/or terminals)",
                      "A → B (only variables allowed on RHS)", "α → β (any string on both sides)"],
                "a": 1,
                "e": "CFG rules are A→α where A is a single variable and α ∈ (V∪Σ)*. The left-hand side is always a single variable.",
                "ce": "A CFG production rule has the form A → α, where A is a single variable (non-terminal) and α is any string of variables and/or terminals."
            },
            {
                "q": "The language of a CFG G, written L(G), is...",
                "c": ["All strings derivable from any variable", "The set of all terminal strings derivable from the start symbol S",
                      "All production rules applied once to S", "All strings that cannot be derived"],
                "a": 1,
                "e": "L(G) = {w ∈ Σ* | S ⟹* w} — all terminal strings reachable from the start variable by any number of rule applications.",
                "ce": "L(G) is the set of all terminal strings derivable from the start symbol S: L(G) = {w ∈ Σ* | S ⟹* w}."
            },
            {
                "q": "Chomsky Normal Form (CNF) requires all productions to be...",
                "c": ["A → a (single terminal) only", "A → BC or A → a (plus S → ε if ε ∈ L(G))",
                      "A → ABC or A → a", "A → B or A → a"],
                "a": 1,
                "e": "CNF: every rule is either A→BC (two variables) or A→a (one terminal). This form is required by algorithms like CYK.",
                "ce": "CNF requires every production to be either A → BC (two non-terminals) or A → a (one terminal), plus S → ε if needed."
            },
            {
                "q": "A grammar is ambiguous if...",
                "c": ["It has more than one start variable", "Some string has two or more distinct parse trees (leftmost derivations)",
                      "It has ε-productions", "It generates an infinite language"],
                "a": 1,
                "e": "Ambiguity: a string w has two different parse trees (equivalently, two different leftmost derivations) in the grammar.",
                "ce": "A grammar is ambiguous if some string has two or more distinct parse trees (equivalently, two distinct leftmost derivations)."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "CFGs generate exactly which class of languages?",
                "c": ["Regular languages", "Context-free languages (CFL)",
                      "Recursively enumerable languages", "Decidable languages"],
                "a": 1,
                "e": "CFGs generate exactly the context-free languages — a strictly larger class than regular languages.",
                "ce": "CFGs generate exactly the context-free languages (CFLs) — a strictly larger class than regular languages, equivalent in power to pushdown automata."
            },
            {
                "q": "Which of the following is true about regular languages and context-free languages?",
                "c": ["Every CFL is also regular", "Every regular language is also context-free (Regular ⊂ CFL)",
                      "They are disjoint classes", "They are the same class"],
                "a": 1,
                "e": "Regular ⊂ CFL (proper subset): every regular language has a CFG, but not every CFL is regular (e.g., {aⁿbⁿ}).",
                "ce": "Every regular language is also context-free (Regular ⊊ CFL), but not every CFL is regular — e.g., {aⁿbⁿ} is CFL but not regular."
            },
            {
                "q": "Which CFG generates {aⁿbⁿ | n ≥ 0}?",
                "c": ["S → ab | ε", "S → aSb | ε", "S → aS | Sb | ε", "S → ab | aabb"],
                "a": 1,
                "e": "S → aSb | ε: applying S→aSb n times then S→ε gives aⁿbⁿ — the recursive rule wraps a's and b's symmetrically.",
                "ce": "S → aSb | ε generates {aⁿbⁿ}: each application of S→aSb adds one a on the left and one b on the right, then S→ε terminates."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "A leftmost derivation always replaces...",
                "c": ["The rightmost variable in the sentential form", "The variable with the most productions",
                      "The leftmost variable in the current sentential form", "The start symbol S"],
                "a": 2,
                "e": "Leftmost derivation: at each step, the leftmost (first) variable in the current string is expanded.",
                "ce": "A leftmost derivation always expands the leftmost (first) remaining variable in the current sentential form."
            },
            {
                "q": "An inherently ambiguous language is one where...",
                "c": ["No CFG exists for it", "Every CFG generating it is ambiguous",
                      "The CYK algorithm fails", "It requires exponential derivations"],
                "a": 1,
                "e": "An inherently ambiguous CFL cannot be generated by any unambiguous CFG — all grammars for it have some ambiguous string.",
                "ce": "An inherently ambiguous language is a CFL for which every possible CFG is ambiguous — no unambiguous grammar exists for it."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "The CYK algorithm decides if w ∈ L(G) for a grammar G in CNF. Its time complexity is...",
                "c": ["O(n)", "O(n²)", "O(n³ · |G|)", "O(2^n)"],
                "a": 2,
                "e": "CYK runs in O(n³ · |G|) time using dynamic programming on substrings of w — cubic in the string length.",
                "ce": "CYK runs in O(n³ · |G|) time: for each substring length, each start position, and each CNF rule, it checks all split points — cubic dynamic programming."
            },
            {
                "q": "Which of the following is NOT a closure property of context-free languages?",
                "c": ["Union", "Concatenation", "Kleene star", "Intersection"],
                "a": 3,
                "e": "CFLs are closed under union, concatenation, and Kleene star — but NOT intersection. The intersection of two CFLs may not be a CFL.",
                "ce": "CFLs are NOT closed under intersection — the intersection of two CFLs can be a non-CFL (e.g., {aⁿbⁿcᵐ} ∩ {aᵐbⁿcⁿ} = {aⁿbⁿcⁿ})."
            },
            {
                "q": "Which of the following is NOT a step in converting a CFG to Chomsky Normal Form?",
                "c": ["Adding a new start symbol S₀ → S",
                      "Eliminating ε-productions (except possibly S → ε)",
                      "Eliminating unit productions (A → B)",
                      "Removing all variables (non-terminals) from the grammar"],
                "a": 3,
                "e": "CNF conversion steps: new start, eliminate ε-productions, eliminate unit productions, convert long rules. Variables are essential — we never remove them.",
                "ce": "CNF conversion never removes all variables — the steps are: add new start, eliminate ε-productions, eliminate unit productions (A→B), then binarize long rules."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "The language {aⁿbⁿcⁿ | n ≥ 0} is not context-free. This is proven using...",
                "c": ["The regular pumping lemma", "The pumping lemma for context-free languages",
                      "Rice's theorem", "The Myhill-Nerode theorem"],
                "a": 1,
                "e": "The CFL pumping lemma: if {aⁿbⁿcⁿ} were CFL, any long string could be pumped — but pumping either the b's or the c's breaks the three-way balance.",
                "ce": "{aⁿbⁿcⁿ} is proven non-CFL by the CFL pumping lemma: any pump of a string aⁿbⁿcⁿ either changes only one or two of the three counts, breaking the required equality."
            },
            {
                "q": "The grammar S → SS | (S) | ε generates the language of balanced parentheses. This grammar is...",
                "c": ["Ambiguous — 'S → SS' allows multiple parse trees for some strings",
                      "Unambiguous — each string has exactly one parse tree",
                      "Not a valid CFG since it has ε-productions",
                      "In Chomsky Normal Form already"],
                "a": 0,
                "e": "S→SS is ambiguous: the string '()()()' has multiple parse trees depending on how the three pairs are grouped.",
                "ce": "The grammar S → SS | (S) | ε is ambiguous because S → SS allows multiple groupings — e.g., '()()()' can be parsed as (SS)S or S(SS)."
            },
            {
                "q": "A unit production in a CFG is a rule of the form...",
                "c": ["A → ε",
                      "A → B (a variable rewrites to a single variable)",
                      "A → BC (a variable rewrites to exactly two variables)",
                      "A → a (a variable rewrites to a single terminal)"],
                "a": 1,
                "e": "Unit productions (A → B) are eliminated during CNF conversion; they create long chains that can be short-circuited without changing the language.",
                "ce": "A unit production is a rule of the form A → B where a variable rewrites to a single variable; these are eliminated during CNF conversion."
            },
            {
                "q": "The CYK table for a string of length n has how many cells to fill?",
                "c": ["n cells", "n² cells", "n(n+1)/2 cells", "n³ cells"],
                "a": 2,
                "e": "CYK fills a triangular table T[i,j] for 1≤i≤j≤n — that's n(n+1)/2 cells (one per substring of w).",
                "ce": "CYK fills a triangular table with one cell per substring of w: T[i,j] for 1 ≤ i ≤ j ≤ n, giving n(n+1)/2 cells total."
            },
            {
                "q": "If h is a homomorphism and L is a context-free language, then h(L) is...",
                "c": ["Always regular",
                      "Always context-free",
                      "Decidable but not necessarily context-free",
                      "Not necessarily context-free"],
                "a": 1,
                "e": "CFLs are closed under homomorphism: if L is CFL and h is any homomorphism, then h(L) = {h(w) | w ∈ L} is also CFL.",
                "ce": "CFLs are closed under homomorphism: if L is a CFL and h is any homomorphism, then h(L) = {h(w) | w ∈ L} is also a CFL."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "A CFG is in Chomsky Normal Form (CNF) if every production is of the form...",
                "c": ["A → a (terminal) or A → BC (two non-terminals); S → ε allowed only if ε ∈ L",
                      "A → aB or A → a (Greibach-style left-terminal)",
                      "A → α for any string α ∈ (V ∪ T)*",
                      "A → ε or A → a (only unit or empty productions)"],
                "a": 0,
                "e": "CNF: every rule is A→BC (two non-terminals) or A→a (one terminal). CNF makes parse trees binary and enables the CYK algorithm.",
                "ce": "CNF requires every rule to be either A → BC (two non-terminals) or A → a (one terminal); S → ε is allowed only if ε ∈ L."
            },
            {
                "q": "The CYK algorithm decides whether w (length n) is in L(G) for a CNF grammar G in time...",
                "c": ["O(n) — linear scan of the string",
                      "O(n² log n) — merge-sort on parse subtrees",
                      "O(n³ |G|) — dynamic programming over all substrings and grammar rules",
                      "Exponential in n"],
                "a": 2,
                "e": "CYK is O(n³ |G|): for each substring length l, each starting position, and each rule A→BC, check every split point k. Bottom-up DP fills an n×n table.",
                "ce": "CYK decides membership in O(n³ |G|) by bottom-up dynamic programming: for each substring length, position, and grammar rule, try every possible split point."
            },
            {
                "q": "A context-free language L is 'inherently ambiguous' if...",
                "c": ["Every CFG for L is ambiguous (some string has ≥2 distinct parse trees) and no unambiguous CFG for L exists",
                      "L cannot be recognized by any deterministic PDA",
                      "L contains strings with multiple parses only for odd-length strings",
                      "L is ambiguous in one grammar but unambiguous in an equivalent grammar"],
                "a": 0,
                "e": "Inherent ambiguity: no equivalent unambiguous CFG exists. Canonical example: L = {aᵢbʲcᵏ | i=j or j=k}. Every CFG must overlap the two sub-languages, causing unavoidable ambiguity for strings with i=j=k.",
                "ce": "A CFL is inherently ambiguous if every CFG generating it is ambiguous — no unambiguous grammar exists for it, not just the particular grammar you have."
            },
            {
                "q": "CFLs are NOT closed under intersection. The standard counterexample is...",
                "c": ["L₁ = {aⁿbⁿ | n≥0} ∩ {bⁿcⁿ | n≥0} = {aⁿbⁿcⁿ} which is not a CFL",
                      "Any two finite languages — their intersection is always non-context-free",
                      "Regular languages — they are context-free and their intersection is non-CFL",
                      "{aⁿ | n is prime} ∩ {aⁿ | n is composite} = ∅"],
                "a": 0,
                "e": "L₁ = {aⁿbⁿcᵐ} and L₂ = {aᵐbⁿcⁿ} are both CFLs. L₁ ∩ L₂ = {aⁿbⁿcⁿ}, which is not a CFL by the CFL Pumping Lemma. CFLs are also not closed under complement.",
                "ce": "The canonical counterexample: {aⁿbⁿcᵐ} ∩ {aᵐbⁿcⁿ} = {aⁿbⁿcⁿ}, which is not a CFL — proving CFLs are not closed under intersection."
            },
            {
                "q": "The correct order of steps when converting a CFG to Chomsky Normal Form is...",
                "c": ["(1) Add new start S₀, (2) eliminate ε-productions, (3) eliminate unit productions, (4) binarize long rules",
                      "(1) Binarize first, (2) eliminate ε-productions, (3) unit productions",
                      "(1) Eliminate unit productions, (2) add new start, (3) ε-productions, (4) binarize",
                      "The order doesn't matter — all steps are independent"],
                "a": 0,
                "e": "Standard order: (1) add S₀→S to isolate the start; (2) eliminate ε-productions; (3) eliminate unit productions A→B; (4) binarize rules A→B₁B₂...Bₖ (k≥3) with fresh non-terminals. Steps interact — order matters.",
                "ce": "The correct CNF conversion order is: (1) add new start S₀, (2) eliminate ε-productions, (3) eliminate unit productions, (4) binarize long rules — the steps must be done in this order."
            },
            {
                "q": "A CFG for palindromes over {a, b} (P = {w | w = wᴿ}) is...",
                "c": ["S → ε | a | b | aSa | bSb  (base: empty/single char; recursive: matching surrounding chars)",
                      "S → ε | ab | ba | SS",
                      "S → a | b | S*",
                      "S → aSb | bSa | ε  (mismatched pairs)"],
                "a": 0,
                "e": "Palindrome CFG: S→ε | a | b | aSa | bSb. A palindrome is empty, a single char, or char c followed by a palindrome followed by c. This generates exactly P. P is CFL but not regular.",
                "ce": "The palindrome CFG is S → ε | a | b | aSa | bSb: base cases handle empty/single-char strings, and the recursive rules wrap matching characters around a shorter palindrome."
            },
        ],
    },

    # ───────────────────────────── PDA ─────────────────────────────
    "PDA": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "What does a PDA have that a finite automaton does not?",
                "c": ["Multiple start states", "An infinite read/write tape",
                      "A stack for additional unbounded memory", "Multiple input alphabets"],
                "a": 2,
                "e": "A PDA has a stack (LIFO memory) in addition to its finite state control, giving it power to count and match nested structures.",
                "ce": "A PDA has a stack (unbounded LIFO memory) in addition to its finite state control, enabling it to count and match nested structures."
            },
            {
                "q": "PDAs recognize exactly which class of languages?",
                "c": ["Regular languages", "Context-free languages",
                      "Decidable languages", "Recursively enumerable languages"],
                "a": 1,
                "e": "The PDA–CFG equivalence theorem: PDAs recognize exactly the context-free languages.",
                "ce": "PDAs recognize exactly the context-free languages — this is the PDA–CFG equivalence theorem."
            },
            {
                "q": "In a PDA transition (q, a, A) → (q', γ), what does A represent?",
                "c": ["The symbol written to the tape", "The symbol read from the top of the stack (popped)",
                      "The new state", "The symbol read from the input"],
                "a": 1,
                "e": "A is the stack symbol that must be on top of the stack for this transition to apply — it is popped as part of the transition.",
                "ce": "In (q, a, A) → (q', γ), A is the stack symbol popped from the top of the stack when this transition fires."
            },
            {
                "q": "In a PDA transition (q, a, A) → (q', γ), what does γ represent?",
                "c": ["The next input symbol to read", "The new state after transition",
                      "The string pushed onto the stack (replacing A)", "The stack bottom marker"],
                "a": 2,
                "e": "γ is pushed onto the stack in place of A. If γ=ε, it is a pure pop; if γ=BA, it pushes B on top and keeps A below.",
                "ce": "In (q, a, A) → (q', γ), γ is the string pushed onto the stack in place of A; γ=ε is a pure pop, γ=BA pushes B on top."
            },
            {
                "q": "A PDA that accepts by empty stack is equivalent to one that accepts by...",
                "c": ["Empty input only", "Final state",
                      "Minimum number of transitions", "Deepest stack depth"],
                "a": 1,
                "e": "Acceptance by empty stack and acceptance by final state are equivalent definitions — every PDA of one type has an equivalent of the other.",
                "ce": "Acceptance by empty stack and acceptance by final state are equivalent — every PDA using one mode has an equivalent PDA using the other mode."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "The bottom-of-stack marker (e.g., Z₀ or $) is used to...",
                "c": ["Mark the first input symbol", "Detect when the stack is empty without physically emptying it",
                      "Indicate the start state", "Prevent the stack from growing"],
                "a": 1,
                "e": "Z₀ is placed at the bottom initially. When it is popped (or visible on top), the PDA knows the stack is otherwise empty.",
                "ce": "The bottom-of-stack marker Z₀ sits at the bottom of the stack; when it becomes visible at the top, the PDA knows the stack is otherwise empty."
            },
            {
                "q": "A deterministic PDA (DPDA) is...",
                "c": ["Equivalent in power to any PDA", "Less powerful than a nondeterministic PDA (recognizes a proper subset of CFLs)",
                      "More powerful than a nondeterministic PDA", "Not a valid model of computation"],
                "a": 1,
                "e": "DPDAs are strictly less powerful than NPDAs. For example, {ww^R} requires nondeterminism — a DPDA cannot recognize it.",
                "ce": "A deterministic PDA (DPDA) is strictly less powerful than a nondeterministic PDA — DPDAs recognize only the deterministic CFLs, a proper subset of all CFLs."
            },
            {
                "q": "A PDA for {aⁿbⁿ | n ≥ 1} works by...",
                "c": ["Counting a's and b's simultaneously in two stacks",
                      "Pushing each 'a' onto the stack, then popping one 'a' for each 'b' read",
                      "Storing the entire input then reading it backwards",
                      "Guessing the midpoint nondeterministically"],
                "a": 1,
                "e": "Push all a's; then for each b, pop one a. Accept if the stack is empty exactly when the input is exhausted.",
                "ce": "A PDA for {aⁿbⁿ} pushes one symbol per 'a', then pops one symbol per 'b', accepting when both the input and stack are simultaneously exhausted."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "A configuration of a PDA is represented as...",
                "c": ["(current state, input read so far)", "(current state, remaining input, stack contents)",
                      "(stack contents, accept/reject status)", "(state, symbol, transition)"],
                "a": 1,
                "e": "A PDA configuration (ID) is a triple (q, w, γ): current state q, remaining input w, current stack γ.",
                "ce": "A PDA configuration (instantaneous description) is the triple (q, w, γ): current state, remaining input string, and current stack contents."
            },
            {
                "q": "Which of these languages CAN be recognized by a nondeterministic PDA?",
                "c": ["{aⁿbⁿcⁿ | n ≥ 0}", "{ww | w ∈ {a,b}*}",
                      "{ww^R | w ∈ {a,b}*} (palindromes)", "{aⁿbⁿcⁿdⁿ | n ≥ 0}"],
                "a": 2,
                "e": "{ww^R} is context-free — a PDA guesses the midpoint nondeterministically, pushes the first half, then matches the second half against the stack.",
                "ce": "{wwᴿ} (palindromes) is recognized by a nondeterministic PDA: guess the midpoint, push the first half, then verify the second half matches the stack in reverse."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "PDAs are to CFGs as DFAs are to...",
                "c": ["Turing machines", "Regular expressions",
                      "Pushdown automata", "Context-free grammars"],
                "a": 1,
                "e": "DFAs ↔ Regular expressions (both characterize regular languages). PDAs ↔ CFGs (both characterize context-free languages).",
                "ce": "PDAs are to CFGs as DFAs are to regular expressions — both pairs are equivalent models for their respective language classes."
            },
            {
                "q": "The equivalence of PDAs and CFGs is proven by...",
                "c": ["Reducing one to a Turing machine and back",
                      "Showing every CFG has an equivalent PDA and every PDA has an equivalent CFG",
                      "Applying the pumping lemma twice", "Using the subset construction"],
                "a": 1,
                "e": "Both directions: CFG → PDA (simulate leftmost derivation on stack) and PDA → CFG (simulate PDA transitions as grammar rules).",
                "ce": "The equivalence is proven in both directions: every CFG has an equivalent PDA (simulate leftmost derivation on the stack), and every PDA has an equivalent CFG."
            },
            {
                "q": "Which language CANNOT be recognized by any PDA (deterministic or nondeterministic)?",
                "c": ["{ww^R | w ∈ {a,b}*}", "{aⁿbⁿ | n ≥ 0}",
                      "{aⁿbⁿcⁿ | n ≥ 0}", "{balanced parentheses}"],
                "a": 2,
                "e": "{aⁿbⁿcⁿ} is not context-free — proven by the CFL pumping lemma. A PDA can't simultaneously count two independent pairs.",
                "ce": "{aⁿbⁿcⁿ} is not context-free and thus cannot be recognized by any PDA — it requires three-way counting that a single stack cannot handle."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "Why can't a DPDA recognize {ww^R | w ∈ {a,b}*}?",
                "c": ["Palindromes require two stacks", "A DPDA cannot tell nondeterministically when the middle of the input is reached",
                      "The alphabet {a,b} is too small", "Palindromes are not context-free"],
                "a": 1,
                "e": "Recognizing palindromes of even length requires guessing the midpoint — a nondeterministic choice that a DPDA cannot make deterministically.",
                "ce": "A DPDA cannot recognize {wwᴿ} because it cannot deterministically identify the midpoint of the input — that requires a nondeterministic guess."
            },
            {
                "q": "In the CFG → PDA construction, the PDA simulates the CFG's leftmost derivation by...",
                "c": ["Storing the entire input on the stack and reading it backwards",
                      "Keeping the current sentential form on the stack and nondeterministically applying grammar rules",
                      "Using states to encode each grammar rule",
                      "Checking all derivations in parallel with multiple stacks"],
                "a": 1,
                "e": "The PDA stores the current sentential form on the stack, nondeterministically expands variables using grammar rules, and matches terminals against input.",
                "ce": "The CFG → PDA construction simulates leftmost derivation: keep the current sentential form on the stack, nondeterministically expand variables with grammar rules, and pop terminals matching the input."
            },
            {
                "q": "A PDA that recognizes {w ∈ {a,b}* | #_a(w) > #_b(w)} works by...",
                "c": ["Pushing one symbol for each 'a' and popping for each 'b'; accepting if the stack is non-empty (and non-empty means only Z₀ plus extras) at the end",
                      "Using two separate stacks to count a's and b's independently",
                      "Counting with states using a finite counter",
                      "Converting to a TM first, then simulating"],
                "a": 0,
                "e": "Push for each 'a' and pop for each 'b' (or vice versa depending on encoding). Accept when input ends and stack still has unmatched a-pushes above Z₀.",
                "ce": "Push a marker for each 'a' and pop for each 'b'; accept when the input ends with unmatched a-markers still on the stack (more a's than b's)."
            },
            {
                "q": "The intersection of a context-free language and a regular language is always...",
                "c": ["Regular",
                      "Context-free",
                      "Decidable but not necessarily context-free",
                      "Context-sensitive but not necessarily context-free"],
                "a": 1,
                "e": "CFL ∩ Regular = CFL (always). Proof: simulate the PDA for the CFL and the DFA for the regular language in parallel — the combined machine is a PDA.",
                "ce": "The intersection of a CFL with a regular language is always a CFL: run the PDA and DFA in parallel — the product is still a PDA."
            },
            {
                "q": "The standard CFG → PDA construction (simulating leftmost derivation) produces a PDA with how many states?",
                "c": ["One state per grammar variable",
                      "One state per terminal symbol",
                      "Three states (q_start, q_loop, q_accept)",
                      "One state per grammar rule"],
                "a": 2,
                "e": "The standard construction uses exactly 3 states: a start state that pushes S and moves to the loop state, a loop state that applies grammar rules nondeterministically, and an accept state reached when the stack holds only Z₀.",
                "ce": "The standard CFG → PDA construction needs only 3 states: a start state, a loop state (where grammar rules are applied nondeterministically), and an accept state."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "A pushdown automaton with two stacks is computationally equivalent to...",
                "c": ["A standard single-stack PDA",
                      "A Turing machine (recognizes all Turing-recognizable languages)",
                      "A linear-bounded automaton",
                      "An ε-NFA"],
                "a": 1,
                "e": "A 2-stack PDA simulates a TM: use one stack for the tape left of the head, the other for the right. Pushing/popping simulates reading and writing. Hence 2-stack PDAs recognize exactly the recursively enumerable languages.",
                "ce": "A 2-stack PDA is equivalent to a Turing machine: one stack holds the tape to the left of the head, the other holds the right — together they simulate the full TM tape."
            },
            {
                "q": "Which language is accepted by a nondeterministic PDA but NOT by any deterministic PDA?",
                "c": ["{aⁿbⁿ | n ≥ 0}",
                      "{wwᴿ | w ∈ {a,b}*}  (even-length palindromes)",
                      "Every regular language",
                      "{aⁿbⁿcⁿ | n ≥ 0}"],
                "a": 1,
                "e": "{wwᴿ}: the NPDA nondeterministically guesses the midpoint, pushes the first half, and matches the second against the stack. No DPDA can determine the midpoint deterministically. This shows DCFL ⊊ CFL.",
                "ce": "{wwᴿ} is accepted by an NPDA (guess midpoint, push first half, match second) but no DPDA can recognize it — demonstrating that DCFL ⊊ CFL."
            },
            {
                "q": "A PDA that accepts 'by empty stack' vs. one that accepts 'by final state' are...",
                "c": ["Different in power — final-state acceptance is strictly more powerful",
                      "Different in power — empty-stack acceptance is strictly more powerful",
                      "Equivalent in power — each mode can simulate the other by adding ε-transitions and a stack-clearing state",
                      "Equivalent only for deterministic PDAs"],
                "a": 2,
                "e": "Both modes are equivalent for nondeterministic PDAs. Empty-stack→final-state: add a new accept state reached when the stack would empty. Final-state→empty-stack: add a bottom marker and a cleanup state.",
                "ce": "Acceptance by empty stack and by final state are equivalent for nondeterministic PDAs — each mode can be converted to the other via simple state/transition additions."
            },
            {
                "q": "The standard 'top-down' construction converting a CFG G to a PDA (accepting L(G) by empty stack) works by...",
                "c": ["Running CYK inside the PDA's transition function",
                      "Starting with S on the stack; if top is non-terminal A, nondeterministically push a right-hand side of an A-production; if top is terminal a, pop and match against input",
                      "Converting G to CNF first, then building a bottom-up chart parser",
                      "Reversing all productions to parse right-to-left"],
                "a": 1,
                "e": "Top-down PDA: push S; loop — if top is non-terminal A, ε-pop A and push an RHS nondeterministically; if top is terminal a, read and match input a. Accept when stack is empty and input exhausted.",
                "ce": "The top-down PDA pushes S, then in a loop: if the top is a non-terminal A, nondeterministically replace it with an A-production's RHS; if it's a terminal a, match and consume input a."
            },
            {
                "q": "The 'triple construction' converting a PDA to a CFG produces non-terminals of the form...",
                "c": ["[A, i] for each non-terminal A and state i",
                      "[p, A, q] representing 'starting in state p with A on top, the PDA can pop A net and reach state q'",
                      "[a, p, q] representing transitions on symbol a from p to q",
                      "One non-terminal per production rule of the PDA"],
                "a": 1,
                "e": "Triple construction: [p, A, q] means 'PDA in state p with A on stack top can eventually pop A and end in state q.' Grammar rules are derived from PDA transitions, producing an equivalent CFG.",
                "ce": "The triple construction converts a PDA to a CFG using non-terminals [p, A, q] representing 'starting in state p with A on stack, the machine can pop A and reach state q'."
            },
            {
                "q": "Which operation on context-free languages is NOT guaranteed to produce a context-free language?",
                "c": ["Union: L₁ ∪ L₂",
                      "Concatenation: L₁ · L₂",
                      "Kleene star: L*",
                      "Intersection: L₁ ∩ L₂"],
                "a": 3,
                "e": "CFLs are closed under union, concatenation, and Kleene star. They are NOT closed under intersection (canonical counterexample: {aⁿbⁿcᵐ} ∩ {aᵐbⁿcⁿ} = {aⁿbⁿcⁿ}, not a CFL). Also not closed under complement.",
                "ce": "CFLs are NOT closed under intersection — {aⁿbⁿcᵐ} ∩ {aᵐbⁿcⁿ} = {aⁿbⁿcⁿ} which is not a CFL — and also not closed under complement."
            },
        ],
    },

    # ───────────────────────────── TM ─────────────────────────────
    "TM": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "How does a Turing Machine differ from a pushdown automaton?",
                "c": ["A TM uses a queue instead of a stack",
                      "A TM has an infinite read/write tape (not just a stack) and can move left or right",
                      "A TM cannot accept any language", "A TM has no start state"],
                "a": 1,
                "e": "A TM's tape is infinite and fully read/write with bidirectional head movement — far more powerful than a PDA's LIFO stack.",
                "ce": "A TM has an infinite read/write tape with bidirectional head movement, unlike a PDA which only has a LIFO stack."
            },
            {
                "q": "The tape head of a standard Turing Machine can move...",
                "c": ["Only right", "Only left", "Left or right", "Left, right, or stay"],
                "a": 2,
                "e": "The standard TM head moves L or R after each step. Some formulations add 'stay', but this adds no extra power.",
                "ce": "The standard TM tape head moves left (L) or right (R) after each step — bidirectional movement is what makes TMs more powerful than PDAs."
            },
            {
                "q": "A TM halts when it enters...",
                "c": ["Any state", "A looping state", "An accept state or a reject state (halt states)",
                      "The start state again"],
                "a": 2,
                "e": "TMs have two designated halt states: q_accept and q_reject. Entering either causes the machine to halt immediately.",
                "ce": "A TM halts immediately upon entering either q_accept (accepting halt) or q_reject (rejecting halt) — these are the only states that terminate computation."
            },
            {
                "q": "The Church-Turing Thesis asserts...",
                "c": ["All languages are decidable", "Any effectively computable function can be computed by a Turing Machine",
                      "Every TM can be simulated by a DFA", "Nondeterministic TMs are more powerful than deterministic TMs"],
                "a": 1,
                "e": "The Church-Turing Thesis (informal): intuitive computability = Turing computability. It is a thesis, not a theorem — it cannot be formally proved.",
                "ce": "The Church-Turing Thesis claims that any effectively computable function can be computed by a Turing Machine — it is an informal thesis, not a proven theorem."
            },
            {
                "q": "A language is Turing-recognizable (recursively enumerable) if...",
                "c": ["Every TM always halts on it", "Some TM accepts every string in it (may loop on strings not in it)",
                      "No TM can recognize it", "It has a polynomial-time algorithm"],
                "a": 1,
                "e": "Turing-recognizable: a TM accepts every string in L, but may loop (never halt) on strings not in L.",
                "ce": "A Turing-recognizable (RE) language has a TM that accepts every string in L, but may loop forever on strings not in L — it is not required to halt and reject."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "A language is decidable (recursive) if...",
                "c": ["Some TM accepts strings in L (and may loop on others)",
                      "Some TM always halts and correctly accepts strings in L and rejects strings not in L",
                      "It can be described by a CFG", "It can be recognized in polynomial time"],
                "a": 1,
                "e": "Decidable: a TM that always halts (a 'decider') that accepts L and rejects its complement — no infinite loops.",
                "ce": "A decidable language has a TM (a decider) that always halts — accepting strings in L and rejecting strings not in L, with no infinite loops."
            },
            {
                "q": "Every decidable language is also...",
                "c": ["Regular", "Context-free", "Turing-recognizable", "NP-complete"],
                "a": 2,
                "e": "Decidable ⊂ Turing-recognizable: a decider always halts, so it is certainly a recognizer. The converse is false.",
                "ce": "Every decidable language is Turing-recognizable because a decider always halts (and thus accepts), but not every Turing-recognizable language is decidable."
            },
            {
                "q": "A nondeterministic Turing Machine (NTM) is equivalent in power to a deterministic TM because...",
                "c": ["NTMs are slower but recognize the same languages",
                      "Every NTM can be simulated by a deterministic TM (e.g., via BFS over computation tree)",
                      "NTMs cannot be constructed in practice", "Deterministic TMs are more powerful"],
                "a": 1,
                "e": "A deterministic TM can simulate an NTM by doing BFS over all nondeterministic branches — same languages, potentially exponential time.",
                "ce": "Every NTM can be simulated by a deterministic TM (via BFS over nondeterministic branches), so NTMs and DTMs recognize exactly the same languages."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "The blank symbol (⊔ or B) on a TM tape represents...",
                "c": ["The end-of-input marker", "An empty tape cell (the tape is blank beyond the input)",
                      "An accept transition", "A separator between input and work area"],
                "a": 1,
                "e": "The tape is infinite and initially blank (⊔) beyond the input. The TM reads blanks to know it has passed the end of the input.",
                "ce": "The blank symbol (⊔) fills all tape cells beyond the input; reading a blank tells the TM it has moved past the end of the input string."
            },
            {
                "q": "Multi-tape Turing Machines are _____ single-tape TMs.",
                "c": ["More powerful than", "Equivalent in power to (same languages decided)",
                      "Less powerful than", "Incomparable with"],
                "a": 1,
                "e": "Multi-tape TMs are equivalent to single-tape TMs in power — any multi-tape TM can be simulated by a single-tape TM (with quadratic overhead).",
                "ce": "Multi-tape TMs are equivalent in power to single-tape TMs — the additional tapes provide speed but not extra language-recognition ability."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "Which of the following is NOT decidable?",
                "c": ["The language of a DFA given as input", "The halting problem {⟨M,w⟩ | M halts on w}",
                      "Membership in a regular language", "Equivalence of two DFAs"],
                "a": 1,
                "e": "The halting problem is undecidable — proven by diagonalization (Turing 1936). DFA and regular language problems are decidable.",
                "ce": "The halting problem {⟨M,w⟩ | M halts on w} is undecidable — proven by Turing's 1936 diagonalization argument."
            },
            {
                "q": "The class of Turing-recognizable languages is also called...",
                "c": ["Regular languages", "Context-free languages",
                      "Recursively enumerable (RE) languages", "Decidable languages"],
                "a": 2,
                "e": "Turing-recognizable = recursively enumerable (RE). Decidable = recursive. These are the classical computability-theory terms.",
                "ce": "Turing-recognizable languages are also called recursively enumerable (RE); decidable languages are also called recursive — these are the classical computability-theory names."
            },
            {
                "q": "The halting problem undecidability proof constructs machine D from a hypothetical decider H. What does D do on input ⟨M⟩?",
                "c": ["Simulates M on a blank tape forever",
                      "Runs H on ⟨M,⟨M⟩⟩; if H accepts (M halts on ⟨M⟩) then D loops; if H rejects, D accepts",
                      "Copies M's tape and runs in reverse",
                      "Converts M to a DFA and accepts if M is regular"],
                "a": 1,
                "e": "D does the opposite of what H predicts for M on its own encoding. When D runs on ⟨D⟩, D accepts iff D doesn't halt — a contradiction.",
                "ce": "D runs H on ⟨M, ⟨M⟩⟩ and does the opposite: if H says M halts on ⟨M⟩, D loops; if H says M doesn't halt, D accepts — creating a contradiction when M = D."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "A language L is decidable if and only if...",
                "c": ["L is Turing-recognizable", "L is finite",
                      "Both L and its complement L̄ are Turing-recognizable",
                      "L can be parsed by a CFG"],
                "a": 2,
                "e": "L decidable ⟺ L is RE and co-RE. If both L and L̄ are recognized, run both recognizers in parallel; whichever accepts first gives the answer.",
                "ce": "L is decidable if and only if both L and its complement L̄ are Turing-recognizable — run both recognizers in parallel; the first to accept determines the answer."
            },
            {
                "q": "Which correctly orders these language classes from LEAST to MOST powerful?",
                "c": ["Regular ⊂ Decidable ⊂ CFL ⊂ RE",
                      "Regular ⊂ CFL ⊂ Decidable ⊂ RE",
                      "CFL ⊂ Regular ⊂ Decidable ⊂ RE",
                      "Regular ⊂ CFL ⊂ RE ⊂ Decidable"],
                "a": 1,
                "e": "The hierarchy: Regular ⊊ CFL ⊊ Decidable ⊊ RE ⊊ All languages. Each is a strict subset of the next.",
                "ce": "The correct language hierarchy from least to most expressive is: Regular ⊊ CFL ⊊ Decidable ⊊ RE ⊊ All languages."
            },
            {
                "q": "A nondeterministic Turing Machine running in time t(n) can be simulated by a deterministic TM in time...",
                "c": ["O(t(n)²)", "O(t(n) · |Q|)", "2^O(t(n))", "O(t(n) · log t(n))"],
                "a": 2,
                "e": "BFS over an NTM's computation tree of depth t(n) and bounded branching factor costs exponential deterministic time: 2^O(t(n)).",
                "ce": "Simulating an NTM with BFS over its computation tree of depth t(n) costs 2^O(t(n)) deterministic time — exponential overhead."
            },
            {
                "q": "A language A is mapping-reducible (many-one reducible) to B — written A ≤_m B — if there exists a computable function f such that...",
                "c": ["For all w: w ∈ A ↔ f(w) ∈ B",
                      "For all w: f(w) ∈ A ↔ w ∈ B",
                      "Some strings in A map to strings in B",
                      "f runs in polynomial time"],
                "a": 0,
                "e": "A ≤_m B: there is a computable total function f where x ∈ A iff f(x) ∈ B. This 'translates' membership questions from A into membership questions about B.",
                "ce": "A ≤_m B means there is a computable function f such that x ∈ A iff f(x) ∈ B for all x — A's membership questions reduce to B's."
            },
            {
                "q": "The complement of a Turing-recognizable language (a co-RE language) is Turing-recognizable if and only if...",
                "c": ["The original language is finite",
                      "The original language is regular",
                      "The original language is decidable",
                      "The original language is NP-complete"],
                "a": 2,
                "e": "co-RE ∩ RE = Decidable: a language is decidable iff both it and its complement are Turing-recognizable. A non-decidable RE language has a non-RE complement.",
                "ce": "The complement of a Turing-recognizable language is Turing-recognizable if and only if the original language is decidable."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "Simulating a k-tape TM on a single-tape TM for input of length n incurs time...",
                "c": ["O(n) — tape heads can be tracked in O(1) per step",
                      "O(t(n)² · k) worst case — each k-tape step requires O(t(n)) sweeps of the single tape to update all virtual heads",
                      "O(2^n) — exponential slowdown is unavoidable",
                      "Exactly the same time as the multi-tape TM"],
                "a": 1,
                "e": "The single tape stores all k tapes interleaved with head markers. Each step of the k-tape TM requires two passes (O(n)) to read all heads and update. For k-tape TM running in time t(n), single-tape runs in O(t(n)² · k).",
                "ce": "Simulating a k-tape TM on a single tape incurs O(t(n)² · k) time: the single tape interleaves all k tapes, and each k-tape step requires O(t(n)) sweeps to update."
            },
            {
                "q": "Simulating a nondeterministic TM (NTM) on a deterministic TM (DTM) incurs a time overhead of...",
                "c": ["O(log n) — only logarithmic overhead",
                      "At most polynomial — NTM and DTM always share the same polynomial time class",
                      "At most exponential — DTM does BFS over all NTM branches (branching factor b, depth t(n)), yielding O(b^t(n)) total work",
                      "No overhead — every NTM step simulates in O(1)"],
                "a": 2,
                "e": "DTM simulates NTM by BFS over all nondeterministic branches. Tree has branching factor b and depth t(n), so O(b^t(n)) nodes. A poly-time NTM maps to an exponential-time DTM — the core P vs NP tension.",
                "ce": "Simulating an NTM on a DTM via BFS incurs O(b^t(n)) time — exponential in the NTM's running time — which is the core reason P vs NP is hard to resolve."
            },
            {
                "q": "The Church-Turing thesis states that...",
                "c": ["Turing machines can decide every mathematical problem",
                      "Every effectively computable function is computable by a Turing machine (a thesis, not a proven theorem)",
                      "The lambda calculus and Turing machines are the same formal system",
                      "Any polynomial-time algorithm can be computed by a TM in O(n²) steps"],
                "a": 1,
                "e": "The Church-Turing thesis is an informal claim: any computation carried out by an 'algorithm' (intuitive notion) can be performed by a TM. It cannot be proved formally since 'effectively computable' has no purely mathematical definition.",
                "ce": "The Church-Turing thesis informally equates effective computability with Turing machine computability — it is a thesis, not a theorem, because 'algorithm' has no formal mathematical definition."
            },
            {
                "q": "A language L is Turing-recognizable but NOT decidable. This means...",
                "c": ["There is a TM that accepts all strings in L and rejects all strings not in L",
                      "There is a TM that accepts every string in L, but for strings not in L the TM may loop forever rather than halt and reject",
                      "There is no TM for L at all",
                      "L is finite and can be recognized by a finite automaton"],
                "a": 1,
                "e": "Turing-recognizable: a TM accepts every string in L but may loop on strings outside L. Decidable requires the TM always halts. Decidable = recognizable AND co-recognizable.",
                "ce": "Turing-recognizable but not decidable means a TM accepts every string in L but may loop forever on strings NOT in L — it never rejects them explicitly."
            },
            {
                "q": "A Linear Bounded Automaton (LBA) is a TM that...",
                "c": ["Has a linear number of states (|Q| = O(n))",
                      "Uses only the tape space occupied by the input — the head cannot move beyond the input boundaries",
                      "Runs in linear time O(n) on all inputs",
                      "Has exactly one stack in addition to a read-only input tape"],
                "a": 1,
                "e": "An LBA is a nondeterministic TM whose head never moves beyond the input boundaries (space = O(n)). LBAs recognize exactly the context-sensitive languages, sitting between PDAs and full TMs in the Chomsky hierarchy.",
                "ce": "A Linear Bounded Automaton (LBA) is a TM restricted to using only the tape space occupied by the input, recognizing exactly the context-sensitive languages."
            },
            {
                "q": "Which TM variant is strictly WEAKER than a standard (bidirectional infinite tape) TM?",
                "c": ["A TM with a semi-infinite tape (bounded on the left)",
                      "A multi-tape TM with k tapes",
                      "A right-only TM (head can only move right, never left)",
                      "A nondeterministic TM"],
                "a": 2,
                "e": "A right-only TM cannot backtrack, so it is equivalent to a DFA — strictly weaker than a standard TM. Semi-infinite tape and multi-tape TMs are equivalent in power to the standard TM.",
                "ce": "A right-only TM (head can only move right) cannot backtrack and is equivalent to a DFA — it is strictly weaker than a standard bidirectional TM."
            },
        ],
    },

    # ───────────────────────────── UTM ─────────────────────────────
    "UTM": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "A Universal Turing Machine (UTM) takes as input...",
                "c": ["Only the input string w", "An encoding ⟨M, w⟩ of a TM M and input w, then simulates M on w",
                      "The source code of any programming language", "A regular expression and a string"],
                "a": 1,
                "e": "A UTM reads ⟨M, w⟩ — an encoding of M followed by w — and simulates M's computation on w step by step.",
                "ce": "A UTM takes the encoding ⟨M, w⟩ as input — M's description followed by input w — and simulates M's computation on w step by step."
            },
            {
                "q": "The significance of the UTM is that...",
                "c": ["It can solve the halting problem", "A single fixed machine can simulate any other TM — basis for programmable computers",
                      "It runs faster than any other TM", "It requires no input"],
                "a": 1,
                "e": "The UTM shows that one universal machine can simulate all others — the theoretical foundation of the stored-program computer.",
                "ce": "One fixed machine can simulate any arbitrary TM by reading M's encoding and executing M's transitions — the theoretical foundation of stored-program computers."
            },
            {
                "q": "If M accepts w, then the UTM on input ⟨M, w⟩ will...",
                "c": ["Loop forever", "Reject ⟨M, w⟩",
                      "Accept ⟨M, w⟩", "Run for exactly |w| steps"],
                "a": 2,
                "e": "The UTM faithfully simulates M. If M accepts w (reaches q_accept), the UTM accepts ⟨M, w⟩.",
                "ce": "The UTM faithfully simulates M, so when M reaches its accept state on w, the UTM likewise accepts its input ⟨M, w⟩."
            },
            {
                "q": "If M loops forever on w, then the UTM on input ⟨M, w⟩ will...",
                "c": ["Accept after a fixed number of steps", "Detect the loop and reject",
                      "Also loop forever", "Output M's description"],
                "a": 2,
                "e": "The UTM's simulation is faithful — if M never halts, the UTM never halts either. This is why the halting problem is undecidable.",
                "ce": "The UTM's simulation is fully faithful — if M never reaches a halting state on w, the UTM's simulation also runs forever."
            },
            {
                "q": "The language A_TM = {⟨M, w⟩ | M accepts w} is...",
                "c": ["Decidable", "Regular", "Turing-recognizable but NOT decidable",
                      "Not Turing-recognizable"],
                "a": 2,
                "e": "The UTM recognizes A_TM (simulate M on w; accept if M accepts). But A_TM is not decidable — the halting problem reduces to it.",
                "ce": "The UTM witnesses recognizability (simulate M on w; accept if M accepts), but no decider exists because the simulation may loop forever when M loops."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "How is a Turing Machine M typically encoded for input to a UTM?",
                "c": ["As a Python program", "As a string over {0,1} encoding M's states, alphabet, and transitions",
                      "As a graph drawing", "As a regular expression"],
                "a": 1,
                "e": "TMs are encoded as strings (e.g., binary) listing states, alphabets, and transition rules. Any reasonable encoding works.",
                "ce": "A TM is encoded as a binary or ASCII string listing all its states, alphabets, and transition rules — any fixed, decodable encoding works, and the UTM can decode and simulate it."
            },
            {
                "q": "Who first described the Universal Turing Machine?",
                "c": ["John von Neumann", "Alan Turing", "Alonzo Church", "Kurt Gödel"],
                "a": 1,
                "e": "Alan Turing described the UTM in his landmark 1936 paper 'On Computable Numbers, with an Application to the Entscheidungsproblem'.",
                "ce": "Alan Turing defined the UTM in his seminal 1936 paper 'On Computable Numbers, with an Application to the Entscheidungsproblem'."
            },
            {
                "q": "The UTM simulates M by maintaining on its tape...",
                "c": ["Only the current state of M",
                      "The encoding of M (its transition table), the simulated tape contents, and M's current state",
                      "The entire computation history of M", "Only the input w"],
                "a": 1,
                "e": "The UTM typically uses multiple tape regions: one for M's description, one for the simulated tape, one for M's current state.",
                "ce": "The UTM maintains separate tape regions for M's transition table, M's current state marker, and the simulated tape contents, so it can look up transitions and update the simulation."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "The undecidability of A_TM implies that...",
                "c": ["No language is decidable",
                      "There is no algorithm that always determines whether an arbitrary program accepts an arbitrary input",
                      "All RE languages are decidable", "Turing machines cannot compute anything useful"],
                "a": 1,
                "e": "A_TM undecidable = the halting-and-accepting problem is unsolvable. This fundamentally limits what automated verification can do.",
                "ce": "A_TM undecidable means no algorithm can always determine whether an arbitrary TM accepts an arbitrary input — the fundamental limit of automated program verification."
            },
            {
                "q": "The UTM is a theoretical ancestor of...",
                "c": ["The DFA", "The pushdown automaton",
                      "Modern stored-program computers (von Neumann architecture)", "Context-free grammars"],
                "a": 2,
                "e": "Von Neumann's stored-program architecture (program stored in memory, same as data) directly mirrors the UTM's design.",
                "ce": "The von Neumann stored-program architecture — where the program is stored in memory just like data — directly mirrors the UTM's design of encoding a machine description on the same tape as the input."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "Rice's Theorem states that for any non-trivial semantic property P of TM languages...",
                "c": ["P is always decidable", "P is always undecidable",
                      "P is decidable only if L is finite", "P can be checked in polynomial time"],
                "a": 1,
                "e": "Rice's Theorem: any non-trivial property of the language recognized by a TM is undecidable. 'Non-trivial' = not true for all TMs or false for all TMs.",
                "ce": "Rice's Theorem says any non-trivial property of the language a TM recognizes is undecidable — 'always undecidable' is the correct characterization."
            },
            {
                "q": "The reduction from the halting problem to A_TM shows...",
                "c": ["The halting problem is easier than A_TM", "If A_TM were decidable, the halting problem would also be decidable",
                      "A_TM is decidable", "Both problems are in P"],
                "a": 1,
                "e": "HALT_TM ≤_m A_TM: a decider for A_TM would give a decider for HALT_TM. Since HALT_TM is undecidable, so is A_TM.",
                "ce": "HALT_TM ≤_m A_TM: modify M to accept whenever it halts, then an A_TM decider decides HALT_TM. So if A_TM were decidable, the halting problem would also be decidable."
            },
            {
                "q": "The proof that A_TM is undecidable uses diagonalization. The key contradiction when D runs on ⟨D⟩ is...",
                "c": ["D loops on its own encoding — but loops are allowed",
                      "D accepts ⟨D⟩ iff D rejects ⟨D⟩ — a logical impossibility, so no decider for A_TM can exist",
                      "D's encoding is too long to process", "D's construction violates the Church-Turing thesis"],
                "a": 1,
                "e": "D(⟨M⟩): accept if H(⟨M,⟨M⟩⟩) rejects; loop if H accepts. When M=D: D accepts ⟨D⟩ ⟺ H says D rejects ⟨D⟩ ⟺ D rejects ⟨D⟩. Contradiction.",
                "ce": "The diagonalizer D accepts ⟨D⟩ iff H predicts D rejects ⟨D⟩, giving D accepts ⟨D⟩ iff D rejects ⟨D⟩ — a logical impossibility that proves no A_TM decider H can exist."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "If A_TM were decidable, which of the following would ALSO become decidable?",
                "c": ["Whether a TM has exactly 5 states",
                      "The halting problem {⟨M,w⟩ | M halts on w}",
                      "Whether a given string is a palindrome",
                      "Whether two regular expressions are equivalent"],
                "a": 1,
                "e": "HALT_TM ≤_m A_TM. To decide halting: modify M to accept on halt; then use A_TM decider. So A_TM decidable implies HALT_TM decidable.",
                "ce": "HALT_TM ≤_m A_TM: build M' that simulates M on w and accepts when M halts. If A_TM were decidable, this construction decides the halting problem."
            },
            {
                "q": "Rice's Theorem applies to 'non-trivial semantic properties'. Which of the following IS a non-trivial semantic property (and therefore undecidable)?",
                "c": ["Whether the TM has an even number of states (structural)",
                      "Whether the TM's encoding is a valid string over {0,1} (syntactic)",
                      "Whether the language recognized by the TM contains the string '101' (semantic)",
                      "Whether the TM's transition function is total (structural)"],
                "a": 2,
                "e": "'Does L(M) contain 101?' is a semantic property of the language — by Rice's Theorem it is undecidable. Structural properties (state count, encoding validity) are not covered by Rice's.",
                "ce": "'Does L(M) contain 101?' is about what M recognizes (semantic), not M's structure — Rice's Theorem applies and makes this property undecidable."
            },
            {
                "q": "Rice's Theorem correctly applies to semantic properties of TM languages, NOT structural properties. Which statement is accurate?",
                "c": ["Rice's Theorem makes all TM properties undecidable, including structural ones",
                      "Rice's Theorem applies only to non-trivial properties about the language L(M), not about the machine M's description",
                      "Rice's Theorem says structural properties are always undecidable",
                      "Rice's Theorem only applies to decidable languages"],
                "a": 1,
                "e": "Rice's Theorem covers only semantic (language) properties. 'Does M have 5 states?' is structural and can be decided by inspecting M's encoding.",
                "ce": "Rice's Theorem covers only semantic properties about L(M), not structural properties about the machine M itself — state count and encoding validity are outside Rice's scope and can be decidable."
            },
            {
                "q": "If A ≤_m B (A many-one reduces to B), which consequence is guaranteed?",
                "c": ["If A is undecidable, then B must be undecidable",
                      "If B is undecidable, then A must be undecidable",
                      "A and B recognize the same language",
                      "B is strictly harder than A in all cases"],
                "a": 0,
                "e": "A ≤_m B means B is at least as hard as A. If A is undecidable then B cannot be decidable (else A would be). Equivalently, B decidable implies A decidable.",
                "ce": "A ≤_m B means B is at least as hard as A: if A is undecidable, a decider for B would give a decider for A, contradiction — so B must also be undecidable."
            },
            {
                "q": "The halting problem HALT_TM and A_TM are related by...",
                "c": ["HALT_TM ≤_m A_TM and A_TM ≤_m HALT_TM (they are many-one equivalent in hardness)",
                      "HALT_TM is strictly harder than A_TM",
                      "A_TM is strictly harder than HALT_TM",
                      "They are computability-incomparable"],
                "a": 0,
                "e": "Both reductions hold: HALT_TM ≤_m A_TM (modify M to accept on halt) and A_TM ≤_m HALT_TM (check if M halts and accepts). They are many-one equivalent.",
                "ce": "Both reductions hold in each direction — HALT_TM ≤_m A_TM and A_TM ≤_m HALT_TM — making them many-one equivalent in Turing degree."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "In Turing machine theory, ⟨M⟩ typically denotes...",
                "c": ["The set of strings accepted by M",
                      "An encoding (description) of Turing machine M as a string over a fixed alphabet",
                      "The number of states in M",
                      "The running time of M on empty input"],
                "a": 1,
                "e": "⟨M⟩ is a string encoding (Gödel number) of TM M — a description of M's states, transitions, and alphabet as a binary/ASCII string. This encoding allows a UTM to take ⟨M⟩ as input and simulate M. Fundamental to all undecidability proofs.",
                "ce": "⟨M⟩ is a string encoding (Gödel numbering) of TM M — its states, alphabet, and transitions serialized as a string — enabling a UTM to receive M as input and simulate it."
            },
            {
                "q": "Rice's Theorem states that for any non-trivial property P of Turing-recognizable languages...",
                "c": ["L_P = {⟨M⟩ | L(M) has property P} is decidable if P is monotone",
                      "L_P = {⟨M⟩ | L(M) has property P} is undecidable — no algorithm can decide whether an arbitrary TM's language has P",
                      "L_P is always Turing-recognizable (semi-decidable)",
                      "L_P is decidable as long as P is expressible in first-order logic"],
                "a": 1,
                "e": "Rice's Theorem: any non-trivial semantic property of Turing-recognizable languages is undecidable. 'Non-trivial' means it holds for some TMs and not others, based on the language — not the machine's internal structure.",
                "ce": "Rice's Theorem: for any non-trivial P, L_P = {⟨M⟩ | L(M) has property P} is undecidable — no algorithm can decide whether an arbitrary TM's language has any non-trivial semantic property."
            },
            {
                "q": "Proving E_TM = {⟨M⟩ | L(M) = ∅} is undecidable uses which reduction?",
                "c": ["E_TM reduces to A_TM in polynomial time",
                      "A_TM reduces to Ē_TM (the complement): given ⟨M,w⟩, build M' that accepts x iff M accepts w; then L(M')≠∅ iff M accepts w",
                      "E_TM is decidable by the CYK algorithm",
                      "E_TM is complete for Σ₂ of the arithmetic hierarchy"],
                "a": 1,
                "e": "Reduction: given ⟨M,w⟩, build M' that ignores input and simulates M on w, accepting iff M accepts w. L(M') = ∅ if M doesn't accept w; L(M') = Σ* if M accepts w. An oracle for E_TM would decide A_TM. So E_TM is undecidable.",
                "ce": "Given ⟨M,w⟩, build M' that ignores its own input and simulates M on w; L(M')≠∅ iff M accepts w. An E_TM oracle would decide A_TM, so A_TM ≤_m Ē_TM, making E_TM undecidable."
            },
            {
                "q": "In the arithmetic hierarchy, A_TM is complete for which level?",
                "c": ["Σ⁰₀ = Δ⁰₁ (the decidable languages)",
                      "Σ⁰₁ (the Turing-recognizable languages)",
                      "Π⁰₁ (the co-Turing-recognizable languages)",
                      "Σ⁰₂ (languages computable with two alternating quantifiers)"],
                "a": 1,
                "e": "A_TM is the canonical Σ⁰₁-complete (recognizable but undecidable) language. Ā_TM is Π⁰₁-complete. E_TM is Π⁰₂-complete. The arithmetic hierarchy stratifies undecidable languages by quantifier alternation depth.",
                "ce": "A_TM is the canonical Σ⁰₁-complete language: Turing-recognizable (the UTM witnesses this) but not decidable, and every Σ⁰₁ language many-one reduces to it."
            },
            {
                "q": "The standard proof that HALT_TM = {⟨M,w⟩ | M halts on w} is undecidable uses...",
                "c": ["A direct diagonalization argument",
                      "A reduction from A_TM to HALT_TM: given ⟨M,w⟩, build M' that simulates M on w; if M accepts, accept; if M rejects, loop. M' halts on w' iff M accepts w.",
                      "A reduction from HALT_TM to A_TM only (not the other direction)",
                      "The Post Correspondence Problem"],
                "a": 1,
                "e": "A_TM ≤_m HALT_TM: construct M' that simulates M on w then accepts (or loops on reject). M' halts iff M accepts w. An oracle for HALT_TM would decide A_TM. Since A_TM is undecidable, so is HALT_TM.",
                "ce": "A_TM ≤_m HALT_TM: build M' that simulates M on w and accepts if M accepts (loops on reject); M' halts iff M accepts w, so a HALT_TM oracle decides A_TM, proving HALT_TM undecidable."
            },
            {
                "q": "An efficient universal TM U simulating M on input w of length n incurs what time overhead vs. M's running time t(n)?",
                "c": ["O(1) — a UTM runs at exactly the same speed as M",
                      "O(t(n) · log t(n)) — nearly-linear overhead using efficient simulation",
                      "O(t(n)²) — quadratic overhead from scanning the tape description on each step",
                      "O(2^{t(n)}) — exponential overhead"],
                "a": 1,
                "e": "An efficient UTM (multi-tape, bit-level encoding) simulates M in O(t(n) log t(n)) — the log factor comes from looking up M's transition function in ⟨M⟩. Simpler single-tape UTMs achieve O(t(n)²).",
                "ce": "An efficient multi-tape UTM incurs O(log t(n)) overhead per simulated step to look up M's transition in ⟨M⟩, giving O(t(n) log t(n)) total — a nearly-linear simulation cost."
            },
        ],
    },

    # ───────────────────────────── P vs NP ─────────────────────────────
    "PNP": {
        "regular": [
            # ── easy (0-7) ──────────────────────────────────────────────
            {
                "q": "P is the class of languages decidable in...",
                "c": ["Exponential time", "Polynomial time by a deterministic TM",
                      "Polynomial space", "Linear time only"],
                "a": 1,
                "e": "P = DTIME(n^k for some k): problems solvable in polynomial time on a deterministic TM — practically 'efficiently solvable'.",
                "ce": "P is defined as DTIME(n^k for some k): languages decidable in polynomial time by a deterministic TM — the formal class of 'efficiently solvable' problems."
            },
            {
                "q": "NP is the class of languages...",
                "c": ["Not solvable by any algorithm", "Decidable in polynomial time by a nondeterministic TM (equivalently, verifiable in polynomial time)",
                      "Solvable in polynomial space", "Solvable in exponential time but not polynomial time"],
                "a": 1,
                "e": "NP = problems verifiable in polynomial time. Equivalently, problems decidable in polynomial time by a nondeterministic TM.",
                "ce": "NP is the class of languages decidable in polynomial time by a nondeterministic TM, equivalently those with solutions verifiable in polynomial time given a certificate."
            },
            {
                "q": "In the context of NP, a 'certificate' is...",
                "c": ["A proof that the problem is NP-complete", "A short witness (proof) that a string is in the language, verifiable in polynomial time",
                      "A polynomial-time algorithm", "A reduction from another problem"],
                "a": 1,
                "e": "A certificate (witness) for x ∈ L is a string c such that a polynomial-time verifier V(x, c) accepts. NP = languages with polynomial certificates.",
                "ce": "A certificate is a short witness c such that a poly-time verifier V(x, c) accepts when x ∈ L — NP is exactly the class of languages with such polynomial-size certificates."
            },
            {
                "q": "The P vs NP question asks...",
                "c": ["Whether NP is finite", "Whether every problem verifiable in polynomial time is also solvable in polynomial time",
                      "Whether P equals PSPACE", "Whether NP-complete problems can be solved in linear time"],
                "a": 1,
                "e": "P vs NP: does P = NP? Can every problem whose solution is quickly checkable also be quickly solved? Arguably the most famous open problem in CS.",
                "ce": "P vs NP asks whether every problem whose solution is verifiable in polynomial time is also solvable in polynomial time — the central open question of CS."
            },
            {
                "q": "The Cook-Levin Theorem states...",
                "c": ["P = NP", "SAT (Boolean satisfiability) is NP-complete",
                      "Every NP problem reduces to the halting problem", "Graph coloring is in P"],
                "a": 1,
                "e": "Cook (1971) and Levin (1973) independently proved SAT is NP-complete — the first NP-completeness result, which opened the door to showing other problems NP-complete.",
                "ce": "Cook (1971) and Levin (1973) independently proved SAT is NP-complete — the first NP-completeness result, which provided the template for reducing NP problems to SAT and then to each other."
            },
            # ── easy+medium overlap (5-7) ────────────────────────────────
            {
                "q": "A problem X is NP-complete if...",
                "c": ["X is in P and is the hardest problem in P",
                      "X is in NP and every problem in NP reduces to X in polynomial time",
                      "X is not in NP", "X cannot be verified in polynomial time"],
                "a": 1,
                "e": "NP-complete = in NP AND NP-hard (every NP problem poly-time reduces to it). These are the 'hardest' problems in NP.",
                "ce": "NP-complete means both in NP (solution verifiable in poly time) and NP-hard (every NP problem poly-time reduces to it), making these the hardest problems in NP."
            },
            {
                "q": "If any single NP-complete problem is solved in polynomial time, then...",
                "c": ["Only that problem is solvable efficiently", "P = NP and every NP problem becomes polynomial-time solvable",
                      "All NP-hard problems are solved too", "The result has no implications for other problems"],
                "a": 1,
                "e": "By definition of NP-completeness, every NP problem reduces to any NP-complete problem in poly time — so one poly-time NP-complete algorithm gives P = NP.",
                "ce": "Every NP problem poly-time reduces to every NP-complete problem, so a single poly-time algorithm for one NP-complete problem immediately gives poly-time algorithms for all of NP, i.e., P = NP."
            },
            {
                "q": "A polynomial-time reduction A ≤_p B means...",
                "c": ["B is easier than A", "If B ∈ P then A ∈ P (solving B efficiently lets us solve A efficiently)",
                      "A and B are the same language", "A is NP-complete"],
                "a": 1,
                "e": "A ≤_p B: there's a poly-time computable function f such that x ∈ A ⟺ f(x) ∈ B. So B being easy implies A is easy.",
                "ce": "A ≤_p B means there is a poly-time computable f with x ∈ A ⟺ f(x) ∈ B, so if B ∈ P then A ∈ P — solving B efficiently gives an efficient algorithm for A."
            },
            # ── medium only (8-9) ───────────────────────────────────────
            {
                "q": "NP-hard means...",
                "c": ["The problem is in NP and is hard to verify", "At least as hard as the hardest NP problems (but the problem itself need not be in NP)",
                      "The problem requires exponential time", "The problem is undecidable"],
                "a": 1,
                "e": "NP-hard: every NP problem reduces to it in poly time. It need not be in NP itself (e.g., HALT_TM is NP-hard but not in NP).",
                "ce": "NP-hard means every NP problem poly-time reduces to it, making it at least as hard as the hardest NP problems — but the problem itself need not be in NP."
            },
            {
                "q": "The current consensus among researchers about P vs NP is...",
                "c": ["P = NP (proven)", "P ≠ NP (strongly believed but NOT yet proven)",
                      "P and NP are the same class by definition", "The question has been proven unanswerable"],
                "a": 1,
                "e": "The vast majority of researchers believe P ≠ NP, but no proof exists. It remains the Clay Millennium Problem ($1M prize).",
                "ce": "P ≠ NP is strongly believed by the vast majority of researchers, but no proof exists — it remains one of the Clay Millennium Problems with a $1M prize."
            },
            # ── medium+hard overlap (10-12) ─────────────────────────────
            {
                "q": "Which of the following problems is known to be in P?",
                "c": ["Graph 3-Coloring", "Boolean SAT", "Primality testing (AKS algorithm)", "Traveling Salesman (optimization)"],
                "a": 2,
                "e": "The AKS algorithm (2002) tests primality in polynomial time, proving PRIMES ∈ P. SAT and 3-Coloring are NP-complete; TSP optimization is NP-hard.",
                "ce": "The AKS primality test (2002) runs in polynomial time, proving PRIMES ∈ P. The other options — SAT, 3-Coloring, TSP — are NP-complete or NP-hard, with no known poly-time algorithms."
            },
            {
                "q": "The known containment relationship between P, NP, and PSPACE is...",
                "c": ["P = NP = PSPACE", "P ⊆ NP ⊆ PSPACE (inclusions known; whether any are strict is open, except P ≠ PSPACE)",
                      "NP ⊆ P ⊆ PSPACE", "PSPACE ⊆ NP ⊆ P"],
                "a": 1,
                "e": "P ⊆ NP ⊆ PSPACE is proven. P ≠ PSPACE is also known, so at least one inclusion is strict — but it's unknown which one (or both).",
                "ce": "P ⊆ NP ⊆ PSPACE is proven, and P ≠ PSPACE is known, so at least one of those inclusions is strict — but whether P ≠ NP, NP ≠ PSPACE, or both remains open."
            },
            {
                "q": "3-SAT is NP-complete. The proof that 3-SAT is NP-hard uses...",
                "c": ["A direct reduction from the halting problem",
                      "A polynomial-time reduction from SAT to 3-SAT (converting any CNF formula to 3-CNF)",
                      "Showing 3-SAT is in P", "Rice's Theorem"],
                "a": 1,
                "e": "SAT ≤_p 3-SAT: any CNF clause with k literals can be converted to O(k) 3-literal clauses in poly time. Since SAT is NP-hard, so is 3-SAT.",
                "ce": "SAT ≤_p 3-SAT via a poly-time clause-splitting reduction: any k-literal CNF clause converts to O(k) 3-literal clauses, so 3-SAT is NP-hard (and it's trivially in NP, hence NP-complete)."
            },
            # ── hard only (13-17) ───────────────────────────────────────
            {
                "q": "If a polynomial-time algorithm is found for the Traveling Salesman Problem (decision version), what follows?",
                "c": ["Only TSP becomes efficiently solvable",
                      "P = NP, and all NP problems become efficiently solvable",
                      "Only NP-complete problems related to graphs are solved",
                      "PSPACE = P"],
                "a": 1,
                "e": "TSP (decision) is NP-complete. A poly-time algorithm for it means P = NP — by definition, every NP problem reduces to TSP in poly time.",
                "ce": "TSP (decision version) is NP-complete, so a poly-time algorithm for it means every NP problem is poly-time solvable via the reduction chain — giving P = NP."
            },
            {
                "q": "Which problem is NOT known to be NP-complete, sitting in a suspected 'NP-intermediate' zone between P and NP-complete?",
                "c": ["3-SAT", "Vertex Cover",
                      "Graph Isomorphism", "Independent Set"],
                "a": 2,
                "e": "Graph Isomorphism is in NP but not known to be NP-complete or in P. Ladner's Theorem says if P≠NP such intermediate problems exist; GI is the prime candidate.",
                "ce": "Graph Isomorphism is in NP but not known to be NP-complete or in P — it sits in the suspected NP-intermediate zone whose existence is guaranteed by Ladner's Theorem if P ≠ NP."
            },
            {
                "q": "The Time Hierarchy Theorem implies which separation?",
                "c": ["P = NP",
                      "P ⊊ EXP (there exist problems solvable in exponential time but provably not in polynomial time)",
                      "NP ⊊ PSPACE",
                      "All problems in EXP are NP-complete"],
                "a": 1,
                "e": "The Time Hierarchy Theorem proves that giving a TM more time strictly increases what it can decide. In particular, DTIME(2^n) strictly contains DTIME(n^k), so P ⊊ EXP.",
                "ce": "The Time Hierarchy Theorem proves more time strictly increases decidable languages; since DTIME(2^n) strictly contains DTIME(n^k) for all k, we get P ⊊ EXP."
            },
            {
                "q": "The NP-completeness of Vertex Cover is most directly established by reducing from...",
                "c": ["3-SAT via a gadget construction",
                      "Independent Set (a set S is independent iff V\\S is a vertex cover)",
                      "Clique via edge complementation",
                      "Hamiltonian Path via degree constraints"],
                "a": 1,
                "e": "Independent Set ≤_p Vertex Cover: S is an independent set of size k iff V\\S is a vertex cover of size n−k. The reduction is a simple complement.",
                "ce": "Independent Set ≤_p Vertex Cover: S is an independent set of size k iff V∖S is a vertex cover of size n−k — a trivial complement reduction establishing Vertex Cover is NP-hard."
            },
            {
                "q": "NP ⊆ PSPACE (NP is contained in PSPACE) because...",
                "c": ["Every polynomial-time algorithm also uses polynomial space",
                      "A nondeterministic poly-time computation uses at most polynomial space per branch, so all branches can be simulated sequentially in polynomial space",
                      "PSPACE contains all decidable problems",
                      "NP problems always use linear space"],
                "a": 1,
                "e": "Each nondeterministic branch of an NP machine runs in poly time, hence uses at most poly space. Trying all branches sequentially reuses the same poly-space workspace.",
                "ce": "Each nondeterministic branch of an NP machine runs in poly time and uses at most poly space; simulating all branches sequentially reuses the same poly-space workspace, so NP ⊆ PSPACE."
            },
            # ── hard extension (18-23) ──────────────────────────────────
            {
                "q": "The Cook-Levin theorem proves SAT is NP-complete by...",
                "c": ["Showing SAT can be solved in polynomial time",
                      "Constructing a poly-time reduction from every NP language L to SAT by encoding an NP verifier's computation as a CNF formula",
                      "Showing SAT reduces to 3-SAT",
                      "Using Rice's theorem to show SAT is undecidable"],
                "a": 1,
                "e": "Cook-Levin (1971/1973): for any L∈NP with verifier V, encode V(x,c) as a CNF formula φ_x such that φ_x is satisfiable iff V accepts for some certificate c. This poly-time reduction proves SAT is NP-hard (and it's in NP), hence NP-complete.",
                "ce": "Cook-Levin encodes the computation tableau of any NP verifier V(x,c) as a CNF formula φ_x satisfiable iff some certificate c makes V accept — a poly-time reduction from every NP language to SAT, proving SAT is NP-hard."
            },
            {
                "q": "co-NP is the class of languages whose complements are in NP. Which statement about co-NP is correct?",
                "c": ["co-NP = NP (proven by symmetry)",
                      "co-NP ≠ NP (proven by diagonalization)",
                      "It is unknown whether NP = co-NP; a proof that NP ≠ co-NP would imply P ≠ NP",
                      "co-NP = P"],
                "a": 2,
                "e": "NP vs co-NP is open. If NP ≠ co-NP then P ≠ NP (since P is closed under complement, P ⊆ NP ∩ co-NP). The canonical co-NP-complete problem is TAUT (is every assignment satisfying?) = complement of SAT.",
                "ce": "Whether NP = co-NP is open; a proof that NP ≠ co-NP would imply P ≠ NP, since P is closed under complement and must sit inside both NP and co-NP."
            },
            {
                "q": "The polynomial hierarchy (PH): if P = NP, then PH...",
                "c": ["Continues to grow indefinitely",
                      "Collapses to P (i.e., PH = P = NP = co-NP = ...)",
                      "Collapses to NP² (second level only)",
                      "Expands to PSPACE"],
                "a": 1,
                "e": "If P = NP then Σ^P_1 = P, so NP^P = P. By induction every level collapses: PH = P. More generally, if PH collapses at any level (where Σ^P_k = Σ^P_{k+1}), then PH = Σ^P_k.",
                "ce": "If P = NP then Σ^P_1 = P, so NP with an NP oracle is still P; by induction every level of the polynomial hierarchy collapses, giving PH = P."
            },
            {
                "q": "BPP (Bounded-error Probabilistic Polynomial time) vs NP: the relationship is...",
                "c": ["BPP ⊆ NP (randomness is a special case of nondeterminism)",
                      "NP ⊆ BPP (if P=NP then BPP=NP)",
                      "BPP and NP are incomparable — neither is known to contain the other; under standard assumptions BPP = P",
                      "BPP = PSPACE"],
                "a": 2,
                "e": "BPP vs NP is open. P ⊆ BPP ⊆ PSPACE and P ⊆ NP ⊆ PH ⊆ PSPACE. No known containment between BPP and NP. Under derandomization conjectures (e.g., one-way functions exist), BPP = P.",
                "ce": "BPP and NP are incomparable — neither is known to contain the other; both sit inside PSPACE, but no known relationship exists between them, and standard derandomization conjectures suggest BPP = P."
            },
            {
                "q": "The PCP Theorem implies that for problems like MAX-3-SAT...",
                "c": ["All NP-complete optimization problems have polynomial-time exact algorithms",
                      "Approximating to within a constant factor is NP-hard — there is a constant-factor approximation barrier",
                      "All NP-hard problems have polynomial-time 2-approximations",
                      "Approximation algorithms cannot run in polynomial time for any NP-hard problem"],
                "a": 1,
                "e": "PCP Theorem (1992): NP = PCP[O(log n), O(1)]. Corollary: approximating MAX-3-SAT to within 7/8+ε is NP-hard. Many NP-hard problems have matching hardness-of-approximation results.",
                "ce": "The PCP Theorem (NP = PCP[O(log n), O(1)]) implies that approximating MAX-3-SAT to within 7/8+ε is NP-hard — approximation to within a constant factor runs into a provable NP-hardness barrier."
            },
            {
                "q": "The identity PSPACE = IP (Interactive Polynomial time) is significant because...",
                "c": ["It proves P = NP since IP trivially equals P",
                      "It shows interactive proof systems with an unbounded prover can decide exactly PSPACE problems — far more than NP",
                      "It collapses PSPACE to NP",
                      "It implies all PSPACE-complete problems are in co-NP"],
                "a": 1,
                "e": "PSPACE = IP (Shamir 1992): a powerful prover can convince a poly-time verifier of any PSPACE fact via interaction. Example: TQBF (quantified Boolean formulas) is PSPACE-complete and has an efficient interactive proof.",
                "ce": "PSPACE = IP (Shamir 1992) shows interactive proof systems with an unbounded prover can decide exactly PSPACE — far beyond NP, including TQBF and other PSPACE-complete problems."
            },
        ],
    },
}
