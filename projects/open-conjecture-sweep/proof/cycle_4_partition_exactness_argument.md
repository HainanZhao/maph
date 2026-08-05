# Cycle 4 partition exactness argument

## Claim boundary

This argument proves that the frozen partition pipeline computes the same
canonical child set as a monolithic global sort/unique, assuming its input
partitions are the exact current level and every generated record implements
the Cycle-3 augmentation. Those mathematical obligations remain covered by the
Cycle-3 retained-path argument and the executable controls.

## Fixed records and partition map

At a fixed depth every state is a 16-byte string. Let (R) be the multiset of
all canonical child records emitted by all current states. Let

\[
 pi:R\longrightarrow\{0,\ldots,63\}
\]

be the low six bits of the frozen 64-bit FNV-1a computation over the complete
16-byte record. Equality of records implies equality of their FNV computation
and hence equality of their partition.

Each expansion worker writes a record (r) only to its private shard for
partition (pi(r)). Because shards are private, concurrent scheduling cannot
interleave or corrupt records. Concatenating the three shards for partition
(j) therefore produces exactly the submultiset

\[
 R_j=\{r\in R:\pi(r)=j\}.
\]

## Partition-union lemma

**Lemma.** If every (R_j) is sorted and adjacent equal records are removed,
the union of the 64 resulting files is exactly the set of distinct records in
(R).

**Proof.** Every emitted record belongs to exactly one (R_j), so it occurs in
that partition before deduplication. Sort/unique retains one copy of each
distinct record present there. Conversely, every retained record came from an
emitted record. Finally, equal records have equal partition values, so no
duplicate can be split across two partition files. Thus the partition files
are disjoint sets whose union is precisely (operatorname{set}(R)). ∎

Applying the lemma after every level gives the same canonical level sequence
as Cycle 3's monolithic global deduplication. The Cycle-3 retained-path lemma
then continues to show that every full cover orbit reaches the final level.

## Executable obligations

The implementation must check record-size alignment on every input file,
recompute and verify the partition of every unique output record, verify strict
lexicographic order within each unique partition, count all raw records and
bytes, and reproduce the frozen tiny and (p=47) level/tuple controls before
frontier execution.
