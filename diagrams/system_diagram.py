from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.generic.device import Mobile, Tablet
from diagrams.onprem.client import User, Client
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python, Go
from diagrams.programming.framework import React
from diagrams.generic.blank import Blank
import os

# グラフの属性設定
graph_attr = {
    "fontsize": "20",
    "bgcolor": "white",
    # 図全体の余白（レイアウトを疎にするため少し広めにとる）
    "pad": "1.5",
    # フォントを ASCII のみの名前に固定して Graphviz のエラーを回避
    "fontname": "Helvetica",
    # ラベル付きエッジとの相性を考えて通常スプラインを利用
    "splines": "spline",
    # ノード間の縦・横の間隔をさらに広げて図を疎にする
    "ranksep": "2.2",
    "nodesep": "1.6",
}

node_attr = {
    "fontsize": "14",
}


def video_edge(label: str = "映像") -> Edge:
    """映像系の線（青）"""
    return Edge(label=label, color="#1f77b4", fontcolor="#1f77b4", penwidth="2")


def webrtc_edge(label: str = "WebRTC") -> Edge:
    """WebRTC 通信（オレンジ）"""
    return Edge(label=label, color="#ff7f0e", fontcolor="#ff7f0e", penwidth="2")


def signaling_edge(label: str = "シグナリング/TURN") -> Edge:
    """WebRTC のシグナリングや TURN など制御信号（オレンジ・点線）"""
    return Edge(label=label, color="#ff7f0e", fontcolor="#ff7f0e", style="dashed", penwidth="2")


def webrtc_video_edge(label: str = "WebRTC(映像)") -> Edge:
    """WebRTC + 映像（紫）"""
    return Edge(label=label, color="#9467bd", fontcolor="#9467bd", penwidth="2")


def control_edge(label: str = "制御") -> Edge:
    """制御系の線（緑・実線：実際にデータをやり取りする制御路）"""
    return Edge(label=label, color="#2ca02c", fontcolor="#2ca02c", penwidth="2")


def connect_edge(label: str = "Connect Protocol") -> Edge:
    """Connect Protocol による制御/通信路（ティール系の実線）"""
    return Edge(label=label, color="#17becf", fontcolor="#17becf", penwidth="2")

def operation_edge(label: str = "操作") -> Edge:
    """ユーザー操作系の線（緑・点線）"""
    return Edge(label=label, color="#2ca02c", fontcolor="#2ca02c", style="dashed", penwidth="2")


def collaboration_edge(label: str = "連携") -> Edge:
    """相互連携を示す線（緑・実線・両端矢印）"""
    return Edge(label=label, color="#2ca02c", fontcolor="#2ca02c", penwidth="2", dir="both")

# 出力ディレクトリを作成（絶対パスで指定して Graphviz の cwd 問題を回避）
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT_DIR, "imgs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_diagram(mode: str) -> None:
    """
    mode に応じて論理図(app)とインフラ図(infra)の両方を描く。
    ノード定義は共通化し、if 文でラベルやタイトルなどを切り替える。
    """
    is_infra = mode == "infra"
    title = "システム構成図" if not is_infra else "インフラ構成図"
    filename = os.path.join(OUTPUT_DIR, f"system_{mode}")

    with Diagram(
        title,
        show=False,
        filename=filename,
        # アプリ図は左→右、インフラ図は上→下に物理階層を縦並びにする
        direction="LR" if not is_infra else "TB",
        graph_attr=graph_attr,
        node_attr=node_attr,
    ):
        # 人
        with Cluster("人"):
            person_label = (
                "オペレーター\n(システム全体を操作する人間のオペレーター)"
                if not is_infra
                else "オペレーター"
            )
            person = User(person_label)

        # カメラ (Lightweight Mode)
        with Cluster(
            "カメラ (Lightweight Mode)",
            # クラスタ内のノードは横並びにする
            graph_attr={"rank": "same"},
        ):
            # カメラ本体はアプリ図のみで明示。インフラ図では Arduino を強調しつつ、
            # その中にサービス（CD/CO）のアイコンも配置する。
            camera_icon_path = os.path.join(ROOT_DIR, "imgs", "icons", "camera.png")
            if not is_infra:
                camera_body = Custom(
                    "カメラ本体\n(実際に撮影を行う物理カメラ)",
                    camera_icon_path,
                )
                cd = Tablet("CD\n(カメラ映像をシステムに取り込むキャプチャデバイス)")
                co = Server("CO\n(PTZやアームを物理制御するカメラ用マイコン)")
            else:
                with Cluster("Arduino (Lightweight)"):
                    arduino_light = Server("Arduino")
                    cd_light = Tablet("CD")
                    co_light = Server("CO")

        # カメラ (Autonomous Mode)
        with Cluster(
            "カメラ (Autonomous Mode)",
            # クラスタ内のノードは横並びにする
            graph_attr={"rank": "same"},
        ):
            if not is_infra:
                camera_body_auto = Custom(
                    "カメラ本体\n(Autonomous Mode時の物理カメラ)",
                    camera_icon_path,
                )
                cd_auto = Tablet("CD (Autonomous)\n(Autonomous Mode時のキャプチャデバイス)")
                co_auto = Server("CO (Autonomous)\n(Autonomous Mode時のカメラ用マイコン)")
                fd_auto = Python("FD (Autonomous)\n(Autonomous Mode時にカメラ側に常駐するFD)")
            else:
                # Autonomous Mode のインフラ構成: Raspberry Pi + k3s と Arduino、
                # それぞれの中に対応するサービスをアイコンごと配置
                with Cluster("Raspberry Pi"):
                    rasp = Server("raspberry pi")
                    k3s = Server("k3s")
                    cd_auto_svc = Tablet("CD (Autonomous)")
                    fd_auto_svc = Python("FD (Autonomous)")
                with Cluster("Arduino (Autonomous)"):
                    arduino_auto = Server("Arduino")
                    co_auto_svc = Server("CO (Autonomous)")

        # Master MF
        with Cluster(
            "Master MF",
            # クラスタ内のノードは横並びにする
            graph_attr={"rank": "same"},
        ):
            if not is_infra:
                cr = Go("CR\n(全ての通信を統括する本当のマスタサーバ)")
                rs = Server("RS\n(WebRTCのマスター兼中継を行うリレーステーション)")
                ep = React("EP\n(MDを制御するブラウザUIシステム)")
                md = Python("MD\n(シネマトグラフィー管理と配信を司るメインディレクター)")
                fd = Python("FD\n(MDの指示から画角を計算しCOを制御するフィルムディレクター)")
            else:
                # Master MF を k8s クラスタとして表現し、その中にサービス群を配置
                with Cluster("k8s Cluster (Master MF)"):
                    k8s_cluster = Server("k8s Node(s)")
                    cr_svc = Go("CR")
                    rs_svc = Server("RS")
                    ep_svc = React("EP")
                    md_svc = Python("MD")
                    fd_svc = Python("FD")

        # 配信PC
        with Cluster("配信PC"):
            if not is_infra:
                # PC / ラップトップ / ミキサーなど配信機材のイメージとしてクライアント端末アイコンを利用
                pc = Client("配信端末\n(PCやラップトップ、ミキサーなどの配信機材)")
            else:
                pc = Client("配信端末")

        # インフラ図では配線は描かず、構成要素のみを示す
        if is_infra:
            return

        # ここから下はアプリケーション構成図用の配線

        # 人 → EP（操作）
        person >> operation_edge(label="操作") >> ep

        # カメラ本体 → CD（WebRTC(映像)）
        camera_body >> webrtc_video_edge() >> cd

        # CD → RS（WebRTC のシグナリング/TURN）
        cd >> signaling_edge() >> rs

        # RS → MD, FD, EP（WebRTC のシグナリング）
        rs >> signaling_edge(label="シグナリング") >> md
        rs >> signaling_edge(label="シグナリング") >> fd
        rs >> signaling_edge(label="シグナリング") >> ep

        # CD → MD, FD, EP（WebRTC・映像）
        cd >> webrtc_video_edge() >> md
        cd >> webrtc_video_edge() >> fd
        cd >> webrtc_video_edge() >> ep

        # EP → CR（Connect Protocol）
        ep >> connect_edge() >> cr

        # CD → CR（Connect Protocol）
        cd >> connect_edge() >> cr

        # MD → CR（Connect Protocol）
        md >> connect_edge() >> cr

        # FD → CR（Connect Protocol）
        fd >> connect_edge() >> cr

        # MD ↔ FD（連携：シネマトグラフィー共有など・両端矢印で表現）
        md >> collaboration_edge(label="連携") >> fd

        # Lightweight Mode: MD → 配信端末（映像）
        md >> video_edge() >> pc

        # Lightweight Mode: FD → CO（制御信号）
        fd >> control_edge() >> co

        # --- カメラ (Autonomous Mode) の接続 ---

        # カメラ本体 (Autonomous) → CD (Autonomous)（WebRTC(映像)）
        camera_body_auto >> webrtc_video_edge() >> cd_auto

        # CD (Autonomous) → RS（WebRTC のシグナリング/TURN）
        cd_auto >> signaling_edge() >> rs

        # RS → FD (Autonomous)（WebRTC のシグナリング）
        rs >> signaling_edge(label="シグナリング") >> fd_auto

        # CD (Autonomous) → MD, FD (Autonomous), EP（WebRTC・映像）
        cd_auto >> webrtc_video_edge() >> md
        cd_auto >> webrtc_video_edge() >> fd_auto
        cd_auto >> webrtc_video_edge() >> ep

        # CD (Autonomous), FD (Autonomous) → CR（Connect Protocol）
        cd_auto >> connect_edge() >> cr
        fd_auto >> connect_edge() >> cr

        # MD ↔ FD (Autonomous)（連携）
        md >> collaboration_edge(label="連携") >> fd_auto

        # FD (Autonomous) → CO (Autonomous)（制御信号）
        fd_auto >> control_edge() >> co_auto


if __name__ == "__main__":
    # app（論理図）と infra（インフラ図）の2種類を同時に出力
    for mode in ("app", "infra"):
        draw_diagram(mode)

