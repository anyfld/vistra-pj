# vistra-pj

## Trivy License Check ワークフロー

このリポジトリには、Trivyを使用したライセンスチェックの再利用可能なGitHub Actionsワークフローが含まれています。

### 使用方法

#### 1. 同じリポジトリ内から呼び出す場合

```yaml
jobs:
  check-license:
    uses: ./.github/workflows/trivy-license-check.yml
    with:
      image_name: 'my-image:latest'
```

#### 2. 他のリポジトリから呼び出す場合（anyfld/vistra-pjのポリシーを自動使用）

```yaml
jobs:
  check-license:
    uses: anyfld/vistra-pj/.github/workflows/trivy-license-check.yml@main
    with:
      image_name: 'my-image:latest'
```

デフォルトで `anyfld/vistra-pj` の `configs/policy/license.rego` が使用されます。

#### 3. 別リポジトリのポリシーを使用する場合

```yaml
jobs:
  check-license:
    uses: anyfld/vistra-pj/.github/workflows/trivy-license-check.yml@main
    with:
      image_name: 'my-image:latest'
      policy_repo: '<org>/common-policies'  # ポリシーリポジトリ
      policy_path: 'policy/license.rego'    # ポリシーリポジトリ内のパス
```

### 入力パラメータ

- `image_name` (必須): スキャンするDockerイメージ名
- `policy_repo` (オプション): ポリシーファイルが含まれるリポジトリ（例: `org/common-policies`）。指定しない場合、`anyfld/vistra-pj` が使用されます。
- `policy_path` (オプション): ポリシーリポジトリ内のポリシーファイルのパス。デフォルトは `configs/policy/license.rego`。
