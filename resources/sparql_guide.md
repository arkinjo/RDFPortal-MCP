# SPARQL Query Guide - Simplified

## The Golden Rule
**Before writing any query:** Can you draw a connected graph of all variables using predicates from the schema? If no → the query will fail or produce false results.

---

## The 3-Step Process

### 1. Check Available Databases
```
Run: list_databases()
```
Identify which database(s) contain your target data.

### 2. Read the Schema (MANDATORY)
```
Run: get_MIE_file(database_name)
```
**Find:**
- What predicates connect your entities
- Example queries showing connection patterns
- Performance tips

**Never skip this step.** No schema = broken queries.

### 3. Build Connected Queries

**Core principle:** Every variable must connect to others via actual predicates.

**Good query structure:**
```sparql
SELECT ?var1 ?var2
WHERE {
  ?var1 predicate1 ?var2 .          # ← Direct connection
  ?var1 property "value" .          # ← Properties
  FILTER(...)                       # ← Filters last
}
```

---

## Common Mistakes to Avoid

### ❌ Disconnected Variables
```sparql
SELECT ?gene ?protein
WHERE {
  ?gene a Gene .
  ?protein a Protein .  # No connection between them!
}
# Result: Every gene × every protein = wrong
```

### ✅ Connected Variables
```sparql
SELECT ?gene ?protein
WHERE {
  ?gene encodesProtein ?protein .  # ← Explicit link
}
```

### ❌ Filter-Only Connection
```sparql
WHERE {
  ?x rdfs:label ?name .
  ?y rdfs:label ?name .  # Sharing a literal ≠ connection
}
```

### ✅ Predicate Connection
```sparql
WHERE {
  ?x relatedTo ?y .      # ← Real relationship from schema
}
```

---

## Red Flags - Stop and Revise If:
- Two SELECT variables have no connecting triple patterns
- Variables only share literal values (not predicates)
- You haven't read the schema yet
- Results seem implausibly large

---

## Query Development Tips

**Start simple, build gradually:**
1. Query one entity type first
2. Add one connection at a time
3. Test before adding complexity

**When presenting queries:**
- Show which predicates connect variables
- Explain the connection path: `?a → (predicate) → ?b`
- Note any validation concerns

---

## If Results Look Wrong

Ask yourself:
1. Do all results share the same unexpected value?
2. Is the result count suspiciously high?
3. Did I verify connections in the schema?

**Fix:** Go back to schema, find the correct connecting predicates.

---

## Quick Reference

| Do This | Not This |
|---------|----------|
| Read schema first | Guess predicates |
| Connect via predicates | Connect via shared literals |
| Explain connections | Assume semantic relationships |
| Start simple | Write complex queries first |

**Remember:** Schema documentation is authoritative. Empty results are better than false positives.