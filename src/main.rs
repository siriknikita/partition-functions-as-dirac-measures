use std::env;
use std::fs;
use std::fs::File;
use std::io::{BufWriter, Write};

#[derive(Debug, Clone)]
struct PartitionRecord {
    partition: Vec<usize>,
    measure: Vec<usize>,
}

fn generate_partitions(n: usize) -> Vec<Vec<usize>> {
    fn helper(
        remaining: usize,
        max_part: usize,
        current: &mut Vec<usize>,
        out: &mut Vec<Vec<usize>>,
    ) {
        if remaining == 0 {
            out.push(current.clone());
            return;
        }

        let upper = remaining.min(max_part);
        for part in (1..=upper).rev() {
            current.push(part);
            helper(remaining - part, part, current, out);
            current.pop();
        }
    }

    let mut out = Vec::new();
    let mut current = Vec::new();
    helper(n, n, &mut current, &mut out);
    out
}

fn partition_to_measure(partition: &[usize], n: usize) -> Vec<usize> {
    let mut measure = vec![0usize; n];
    for &part in partition {
        measure[part - 1] += 1;
    }
    measure
}

fn to_json_string(n: usize, records: &[PartitionRecord], aggregate: &[usize]) -> String {
    let mut s = String::new();
    s.push_str("{\n");
    s.push_str(&format!("  \"n\": {},\n", n));

    s.push_str("  \"partitions\": [\n");
    for (i, record) in records.iter().enumerate() {
        s.push_str("    {\n");

        s.push_str("      \"partition\": [");
        for (j, value) in record.partition.iter().enumerate() {
            if j > 0 {
                s.push_str(", ");
            }
            s.push_str(&value.to_string());
        }
        s.push_str("],\n");

        s.push_str("      \"measure\": [");
        for (j, value) in record.measure.iter().enumerate() {
            if j > 0 {
                s.push_str(", ");
            }
            s.push_str(&value.to_string());
        }
        s.push_str("]\n");

        s.push_str("    }");
        if i + 1 < records.len() {
            s.push(',');
        }
        s.push('\n');
    }
    s.push_str("  ],\n");

    s.push_str("  \"aggregate_measure\": [");
    for (i, value) in aggregate.iter().enumerate() {
        if i > 0 {
            s.push_str(", ");
        }
        s.push_str(&value.to_string());
    }
    s.push_str("]\n");

    s.push_str("}\n");
    s
}

fn main() -> std::io::Result<()> {
    let n: usize = env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(12);

    let partitions = generate_partitions(n);

    let mut records = Vec::new();
    let mut aggregate = vec![0usize; n];

    for partition in partitions {
        let measure = partition_to_measure(&partition, n);

        for i in 0..n {
            aggregate[i] += measure[i];
        }

        records.push(PartitionRecord { partition, measure });
    }

    let json = to_json_string(n, &records, &aggregate);

    let out_dir = format!("output/n{n}");
    fs::create_dir_all(&out_dir)?;
    let out_path = format!("{}/partitions_measures.json", out_dir);

    let file = File::create(&out_path)?;
    let mut writer = BufWriter::new(file);
    writer.write_all(json.as_bytes())?;
    writer.flush()?;

    println!("Saved {}", out_path);
    println!("n = {}", n);
    println!("number of partitions = {}", records.len());

    Ok(())
}
