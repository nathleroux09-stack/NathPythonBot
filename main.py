import chess
import chess.polyglot
import time
import random
import requests
import json
import threading

# ==============================================================================
# CONFIGURATION LICHESS
# ==============================================================================
montoken = "lip_U71EPJtbVXcTRdoNo5xc"  # <-- Place ton token Lichess ici

# ==============================================================================
# 1. LIVRE D'OUVERTURES
# ==============================================================================
OPENING_BOOK = {
    # ==========================================
    # 1. LES OUVERTURES LIÉES À 1.e4 e5
    # ==========================================
    "e2e4": {
        "e7e5": {
            # --- 2. Nf3 ---
            "g1f3": {
                "b8c6": {
                    # --- A. RUY LOPEZ (Espagnole) ---
                    "f1b5": {
                        "a7a6": {  # Variante Morphy
                            "b5a4": {
                                "g8f6": {
                                    "e1g1": {
                                        "f8e7": {
                                            "f1e1": {
                                                "b7b5": {
                                                    "a4b3": {
                                                        "d7d6": {
                                                            "c2c3": ["e8g8", "h7h6"]  # Lignes fermées espagnoles
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "f6e4": {  # Variante Ouverte
                                            "d2d4": {
                                                "b7b5": {
                                                    "a4b3": {
                                                        "d7d5": {
                                                            "d4e5": ["c8e6", "f8e7"]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "g8f6": {  # Défense Berlinoise
                            "e1g1": {
                                "f6e4": {
                                    "d2d4": {
                                        "e4d6": {
                                            "b5c6": {
                                                "d7c6": {
                                                    "d4e5": {
                                                        "d6f5": {
                                                            "d1d8": ["e8d8"]  # Finale de la Berlin
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    
                    # --- B. ITALIAN GAME (Italienne) ---
                    "f1c4": {
                        "f8c5": {  # Giuoco Piano
                            "c2c3": {
                                "g8f6": {
                                    "d2d3": {
                                        "d7d6": {
                                            "e1g1": {
                                                "a7a6": {
                                                    "c4b3": ["c5a7", "e8g8"]
                                                }
                                            }
                                        }
                                    },
                                    "d2d4": {  # Ligne agressive classique
                                        "e5d4": {
                                            "c3d4": {
                                                "c5b4": {
                                                    "b1c3": {
                                                        "f6e4": {
                                                            "e1g1": ["b4c3", "d7d5"]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "b2b4": ["c5b6", "c5b4"]  # Gambit Evans
                        },
                        "g8f6": {  # Défense des 2 cavaliers
                            "g1g5": {  # Attaque Fegatello / Fried Liver
                                "d7d5": {
                                    "e4d5": {
                                        "c6a5": {
                                            "c4b5": {
                                                "c2c6": {
                                                    "d5c6": {
                                                        "b7c6": {
                                                            "b5e2": ["h7h6"]
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "f6d5": {
                                            "d2d4": ["e5d4"]
                                        }
                                    }
                                }
                            },
                            "d2d3": {  # Cavalier tranquille
                                "f8c5": {
                                    "c2c3": {
                                        "d7d6": ["e1g1"]
                                    }
                                }
                            }
                        }
                    },
                    
                    # --- C. OUVERTURE DES 4 CAVALIERS ---
                    "b1c3": {
                        "g8f6": {
                            "f1b5": {  # Ligne symétrique
                                "f8b4": {
                                    "e1g1": {
                                        "e8g8": {
                                            "d2d3": {
                                                "d7d6": {
                                                    "c1g5": {
                                                        "b4c3": {
                                                            "b2b3": ["d8e7"]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "d2d4": {  # Variante Écossaise des 4 cavaliers
                                "e5d4": {
                                    "c3d4": {
                                        "f8b4": {
                                            "d4c6": {
                                                "b7c6": {
                                                    "f1d3": ["d7d5"]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            
            # --- D. GAMBIT ROI ---
            "f2f4": {
                "e5f4": {  # Gambit Roi Accepté
                    "g1f3": {
                        "g7g5": {  # Ligne classique
                            "f1c4": {
                                "g5g4": {
                                    "e1g1": {  # Gambit Muzio
                                        "g4f3": {
                                            "d1f3": {
                                                "d8f6": {
                                                    "e4e5": ["f6e5"]
                                                }
                                            }
                                        }
                                    },
                                    "g5g4": ["f6e7"]
                                },
                                "f8g7": {
                                    "d2d4": {
                                        "d7d6": {
                                            "c2c3": ["h7h6"]
                                        }
                                    }
                                }
                            }
                        },
                        "d7d6": {  # Défense Fischer
                            "d2d4": {
                                "g7g5": {
                                    "h2h4": {
                                        "g5g4": ["f3g5"]
                                    }
                                }
                            }
                        }
                    }
                },
                "d7d5": {  # Contre-gambit Falkbeer
                    "e4d5": {
                        "e5e4": {
                            "d2d3": {
                                "g8f6": {
                                    "b1d2": {
                                        "e4d3": {
                                            "f1d3": ["f6d5"]
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        
        # ==========================================
        # 2. DEFENSE FRANÇAISE
        # ==========================================
        "e7e6": {
            "d2d4": {
                "d7d5": {
                    "e4e5": {  # Variante d'Avance
                        "c7c5": {
                            "c2c3": {
                                "b8c6": {
                                    "g1f3": {
                                        "c8d7": {
                                            "f1e2": {
                                                "g8e7": {
                                                    "b1a3": {
                                                        "c5d4": {
                                                            "c3d4": ["e7f5"]
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "d8b6": {
                                            "a2a3": {
                                                "c5c4": {
                                                    "b1d2": ["b8a5"]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "b1c3": {  # Variante principale (Paulsen)
                        "g8f6": {  # Ligne classique
                            "c1g5": {
                                "f8e7": {
                                    "e4e5": {
                                        "f6d7": {
                                            "g5e7": {
                                                "d8e7": {
                                                    "f2f4": {
                                                        "e1g1": ["c7c5"]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "e4e5": {  # Attaque Steinitz
                                "f6d7": {
                                    "f2f4": {
                                        "c7c5": {
                                            "g1f3": {
                                                "b8c6": {
                                                    "c1e3": ["a7a6", "c5d4"]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "f8b4": {  # Variante Winawer
                            "e4e5": {
                                "c7c5": {
                                    "a2a3": {
                                        "b4c3": {
                                            "b2b3": {
                                                "g8e7": {
                                                    "d1g4": {
                                                        "d8c7": ["g4g7"]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "b1d2": {  # Variante Tarrasch
                        "c7c5": {
                            "e4d5": {
                                "e6d5": {
                                    "g1f3": {
                                        "b8c6": {
                                            "f1b5": {
                                                "f8d6": {
                                                    "d4c5": {
                                                        "d6c5": {
                                                            "e1g1": ["g8e7"]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "g8f6": {
                            "e4e5": {
                                "f6d7": {
                                    "f2f4": {
                                        "c7c5": {
                                            "c2c3": {
                                                "b8c6": {
                                                    "d2f3": ["d8b6"]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    
    # ==========================================
    # 3. LES OUVERTURES LIÉES À 1.d4
    # ==========================================
    "d2d4": {
        # --- E. DEFENSE EST-INDIENNE ---
        "g8f6": {
            "c2c4": {
                "g7g6": {
                    "b1c3": {
                        "f8g7": {
                            "e2e4": {
                                "d7d6": {
                                    "g1f3": {  # Variante Classique
                                        "e1g1": {
                                            "f1e2": {
                                                "e7e5": {
                                                    "e1g1": {
                                                        "b8c6": {
                                                            "d4d5": {
                                                                "c6e7": {
                                                                    "f3e1": ["f6d7", "f6e8"]  # Mar del Plata
                                                                }
                                                             }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "f2f3": {  # Variante Sämisch
                                        "e1g1": {
                                            "c1e3": {
                                                "e7e5": {
                                                    "d4d5": {
                                                        "f6h5": {
                                                            "d1d2": {
                                                                "f2f5": ["e1c1"]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "f2f4": {  # Attaque des 4 pions
                                        "e1g1": {
                                            "g1f3": {
                                                "c7c5": {
                                                    "f1e2": {
                                                        "e7e6": {
                                                            "d4d5": {
                                                                "e6d5": ["c4d5"]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        
        # --- F. GAMBIT DAME ---
        "d7d5": {
            "c2c4": {
                "e7e6": {  # Gambit Dame Refusé
                    "b1c3": {
                        "g8f6": {
                            "c1g5": {
                                "f8e7": {
                                    "e2e3": {
                                        "e1g1": {
                                            "g1f3": {
                                                "h7h6": {
                                                    "g5f6": {
                                                        "e7f6": ["c4d5", "a2a3"]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "g1f3": {
                                "f8b4": {  # Variante Ragozine
                                    "c4d5": {
                                        "e6d5": {
                                            "c1g5": {
                                                "h7h6": ["g5f6"]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "c7c6": {  # Défense Slave
                    "g1f3": {
                        "g8f6": {
                            "b1c3": {
                                "e7e6": {  # Semi-Slave
                                    "e2e3": {
                                        "b8d7": {
                                            "f1d3": {
                                                "d5c4": {
                                                    "f1c4": {
                                                        "b7b5": ["c4d3"]  # Variante Meran
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "d5c4": {  # Slave Acceptée Principale
                                    "a2a4": {
                                        "c1f4": {
                                            "b8c6": {
                                                "e2e3": ["c8f5"]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "d5c4": {  # Gambit Dame Accepté
                    "g1f3": {
                        "g8f6": {
                            "e2e3": {
                                "e7e6": {
                                    "f1c4": {
                                        "c7c5": {
                                            "e1g1": {
                                                "a2a3": {
                                                    "c5d4": ["e3d4"]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

def get_book_move(board):
    move_history = [m.uci() for m in board.move_stack]
    current_node = OPENING_BOOK
    
    for move in move_history:
        if isinstance(current_node, dict) and move in current_node:
            current_node = current_node[move]
        else:
            return None
            
    if isinstance(current_node, dict):
        possible_moves = list(current_node.keys())
    elif isinstance(current_node, list):
        possible_moves = current_node
    else:
        return None
        
    if possible_moves:
        chosen = random.choice(possible_moves)
        move = chess.Move.from_uci(chosen)
        if move in board.legal_moves:
            return move
    return None

# ==============================================================================
# 2. FONCTION D'ÉVALUATION (HCE)
# ==============================================================================
PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 300, chess.BISHOP: 300,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

BONUS_BISHOP_PAIR = 30
BONUS_BISHOP_OPEN_PER_MISSING_PAWN = 3
BONUS_KNIGHT_CLOSED_PER_PAWN = 2
BONUS_ROOK_OPEN_FILE = 20
BONUS_ROOK_SEMI_OPEN = 10
BONUS_ROOK_7TH_RANK = 25
BONUS_TEMPO = 15

PENALTY_BISHOP_BLOCKED_BY_PAWN = -15
PENALTY_ISOLATED_PAWN_MG = -15
PENALTY_ISOLATED_PAWN_EG = -20
PENALTY_DOUBLED_PAWN_MG = -15
PENALTY_DOUBLED_PAWN_EG = -20

PASSED_PAWN_BONUS_MG = [0, 0, 10, 20, 40, 70, 100, 0]
PASSED_PAWN_BONUS_EG = [0, 10, 20, 40, 70, 110, 160, 0]

PST_PAWN_MG = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
PST_PAWN_EG = [
    0,  0,  0,  0,  0,  0,  0,  0,
    80, 80, 80, 80, 80, 80, 80, 80,
    50, 50, 50, 50, 50, 50, 50, 50,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    0,  0,  0,  0,  0,  0,  0,  0
]
PST_KNIGHT = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]
PST_BISHOP = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]
PST_ROOK = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
]
PST_KING_MG = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]
PST_KING_EG = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

def evaluate_board(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_game_over():
        return 0

    mg_white, mg_black = 0, 0
    eg_white, eg_black = 0, 0
    game_phase = 0

    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    white_pawns_files = [chess.square_file(sq) for sq in white_pawns]
    black_pawns_files = [chess.square_file(sq) for sq in black_pawns]

    total_pawns = len(white_pawns) + len(black_pawns)
    bishop_open_bonus = max(0, (16 - total_pawns) * BONUS_BISHOP_OPEN_PER_MISSING_PAWN)
    knight_closed_bonus = total_pawns * BONUS_KNIGHT_CLOSED_PER_PAWN

    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        mg_white += BONUS_BISHOP_PAIR; eg_white += BONUS_BISHOP_PAIR
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        mg_black += BONUS_BISHOP_PAIR; eg_black += BONUS_BISHOP_PAIR

    if board.turn == chess.WHITE:
        mg_white += BONUS_TEMPO
    else:
        mg_black += BONUS_TEMPO

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        p_type = piece.piece_type
        color = piece.color
        file_idx = chess.square_file(square)
        rank_idx = chess.square_rank(square)
        pst_square = square if color == chess.WHITE else chess.square_mirror(square)

        v_mg = PIECE_VALUES[p_type]
        v_eg = PIECE_VALUES[p_type]

        if p_type == chess.PAWN:
            v_mg += PST_PAWN_MG[pst_square]
            v_eg += PST_PAWN_EG[pst_square]
            p_files = white_pawns_files if color == chess.WHITE else black_pawns_files
            opp_pawns = black_pawns if color == chess.WHITE else white_pawns

            if p_files.count(file_idx) > 1:
                v_mg += PENALTY_DOUBLED_PAWN_MG
                v_eg += PENALTY_DOUBLED_PAWN_EG

            has_neighbors = False
            if file_idx > 0 and (file_idx - 1) in p_files: has_neighbors = True
            if file_idx < 7 and (file_idx + 1) in p_files: has_neighbors = True
            if not has_neighbors:
                v_mg += PENALTY_ISOLATED_PAWN_MG
                v_eg += PENALTY_ISOLATED_PAWN_EG

            is_passed = True
            for opp_sq in opp_pawns:
                opp_f = chess.square_file(opp_sq)
                opp_r = chess.square_rank(opp_sq)
                if abs(opp_f - file_idx) <= 1:
                    if color == chess.WHITE and opp_r > rank_idx:
                        is_passed = False; break
                    elif color == chess.BLACK and opp_r < rank_idx:
                        is_passed = False; break
            if is_passed:
                rel_rank = rank_idx if color == chess.WHITE else (7 - rank_idx)
                v_mg += PASSED_PAWN_BONUS_MG[rel_rank]
                v_eg += PASSED_PAWN_BONUS_EG[rel_rank]

        elif p_type == chess.KNIGHT:
            v_mg += PST_KNIGHT[pst_square] + knight_closed_bonus
            v_eg += PST_KNIGHT[pst_square] + knight_closed_bonus
            game_phase += 1

        elif p_type == chess.BISHOP:
            v_mg += PST_BISHOP[pst_square] + bishop_open_bonus
            v_eg += PST_BISHOP[pst_square] + bishop_open_bonus
            friendly_pawns = white_pawns if color == chess.WHITE else black_pawns
            if color == chess.WHITE and rank_idx < 7:
                if file_idx > 0 and chess.square(file_idx - 1, rank_idx + 1) in friendly_pawns:
                    v_mg += PENALTY_BISHOP_BLOCKED_BY_PAWN; v_eg += PENALTY_BISHOP_BLOCKED_BY_PAWN
                if file_idx < 7 and chess.square(file_idx + 1, rank_idx + 1) in friendly_pawns:
                    v_mg += PENALTY_BISHOP_BLOCKED_BY_PAWN; v_eg += PENALTY_BISHOP_BLOCKED_BY_PAWN
            elif color == chess.BLACK and rank_idx > 0:
                if file_idx > 0 and chess.square(file_idx - 1, rank_idx - 1) in friendly_pawns:
                    v_mg += PENALTY_BISHOP_BLOCKED_BY_PAWN; v_eg += PENALTY_BISHOP_BLOCKED_BY_PAWN
                if file_idx < 7 and chess.square(file_idx + 1, rank_idx - 1) in friendly_pawns:
                    v_mg += PENALTY_BISHOP_BLOCKED_BY_PAWN; v_eg += PENALTY_BISHOP_BLOCKED_BY_PAWN
            game_phase += 1

        elif p_type == chess.ROOK:
            v_mg += PST_ROOK[pst_square]
            v_eg += PST_ROOK[pst_square]
            game_phase += 2
            friendly_has_pawn = file_idx in (white_pawns_files if color == chess.WHITE else black_pawns_files)
            enemy_has_pawn = file_idx in (black_pawns_files if color == chess.WHITE else white_pawns_files)
            if not friendly_has_pawn and not enemy_has_pawn:
                v_mg += BONUS_ROOK_OPEN_FILE; v_eg += BONUS_ROOK_OPEN_FILE
            elif not friendly_has_pawn:
                v_mg += BONUS_ROOK_SEMI_OPEN; v_eg += BONUS_ROOK_SEMI_OPEN
            if (color == chess.WHITE and rank_idx == 6) or (color == chess.BLACK and rank_idx == 1):
                v_mg += BONUS_ROOK_7TH_RANK; v_eg += BONUS_ROOK_7TH_RANK

        elif p_type == chess.QUEEN:
            game_phase += 4

        elif p_type == chess.KING:
            v_mg += PST_KING_MG[pst_square]
            v_eg += PST_KING_EG[pst_square]

        if color == chess.WHITE:
            mg_white += v_mg; eg_white += v_eg
        else:
            mg_black += v_mg; eg_black += v_eg

    for col, p_set in [(chess.WHITE, white_pawns), (chess.BLACK, black_pawns)]:
        k_sq = board.king(col)
        if k_sq is not None:
            kf = chess.square_file(k_sq)
            kr = chess.square_rank(k_sq)
            shield_bonus = 0
            if (col == chess.WHITE and kr <= 2) or (col == chess.BLACK and kr >= 5):
                t_rank1 = kr + 1 if col == chess.WHITE else kr - 1
                t_rank2 = kr + 2 if col == chess.WHITE else kr - 2
                for f_offset in [-1, 0, 1]:
                    target_f = kf + f_offset
                    if 0 <= target_f <= 7:
                        if chess.square(target_f, t_rank1) in p_set:
                            shield_bonus += 15
                        elif 0 <= t_rank2 <= 7 and chess.square(target_f, t_rank2) in p_set:
                            shield_bonus += 8
            if col == chess.WHITE: mg_white += shield_bonus
            else: mg_black += shield_bonus

    mobility = len(list(board.legal_moves))
    mobility_bonus = mobility * 2
    if board.turn == chess.WHITE: mg_white += mobility_bonus
    else: mg_black += mobility_bonus

    mg_score = mg_white - mg_black
    eg_score = eg_white - eg_black
    if game_phase > 24: game_phase = 24
    mg_weight = game_phase
    eg_weight = 24 - game_phase
    
    score = (mg_score * mg_weight + eg_score * eg_weight) / 24
    return score if board.turn == chess.WHITE else -score

# ==============================================================================
# 3. ORDONNANCEMENT DES COUPS
# ==============================================================================
def score_move(board, move):
    if board.is_castling(move): return 50
    score = 0
    if board.is_capture(move):
        attacker = board.piece_at(move.from_square)
        victim = board.piece_at(move.to_square)
        attacker_val = PIECE_VALUES[attacker.piece_type] if attacker else 0
        victim_val = PIECE_VALUES[victim.piece_type] if victim else 100
        score += 10000 + (victim_val - attacker_val // 10)
    if move.promotion: score += 9000
    if board.gives_check(move): score += 500
    if move.to_square in [chess.D4, chess.E4, chess.D5, chess.E5]: score += 30
    return score

def order_moves(board, moves):
    return sorted(moves, key=lambda m: score_move(board, m), reverse=True)

# ==============================================================================
# 4. ENGINE DE RECHERCHE ALPHABETA
# ==============================================================================
class ChessEngine:
    def __init__(self):
        self.transposition_table = {}
        self.time_limit = 5.0  
        self.start_time = 0
        self.abort_search = False

    def clear_tt(self):
        self.transposition_table.clear()

    def quiescence_search(self, board, alpha, beta):
        stand_pat = evaluate_board(board)
        if stand_pat >= beta: return beta
        if alpha < stand_pat: alpha = stand_pat
        capture_moves = [m for m in board.legal_moves if board.is_capture(m)]
        ordered_captures = order_moves(board, capture_moves)
        for move in ordered_captures:
            board.push(move)
            score = -self.quiescence_search(board, -beta, -alpha)
            board.pop()
            if score >= beta: return beta
            if score > alpha: alpha = score
        return alpha

    def alpha_beta(self, board, depth, alpha, beta):
        if time.time() - self.start_time > self.time_limit:
            self.abort_search = True
            return alpha

        board_hash = chess.polyglot.zobrist_hash(board)
        if board_hash in self.transposition_table:
            tt_entry = self.transposition_table[board_hash]
            if tt_entry['depth'] >= depth:
                if tt_entry['flag'] == 'EXACT': return tt_entry['score']
                elif tt_entry['flag'] == 'LOWERBOUND' and tt_entry['score'] >= beta: return tt_entry['score']
                elif tt_entry['flag'] == 'UPPERBOUND' and tt_entry['score'] <= alpha: return tt_entry['score']

        if depth == 0: return self.quiescence_search(board, alpha, beta)
        if board.is_game_over(): return evaluate_board(board)

        moves = order_moves(board, list(board.legal_moves))
        best_score = -float('inf')
        best_move = None
        old_alpha = alpha

        for move in moves:
            board.push(move)
            score = -self.alpha_beta(board, depth - 1, -beta, -alpha)
            board.pop()
            if self.abort_search: return alpha
            if score > best_score:
                best_score = score
                best_move = move
            if score > alpha: alpha = score
            if alpha >= beta:
                self.transposition_table[board_hash] = {
                    'depth': depth, 'score': best_score, 'flag': 'LOWERBOUND', 'move': best_move
                }
                return best_score

        flag = 'UPPERBOUND' if best_score <= old_alpha else ('LOWERBOUND' if best_score >= beta else 'EXACT')
        self.transposition_table[board_hash] = {
            'depth': depth, 'score': best_score, 'flag': flag, 'move': best_move
        }
        return best_score

    def search_best_move(self, board):
        self.start_time = time.time()
        self.abort_search = False
        
        book_move = get_book_move(board)
        if book_move:
            print("[Moteur] Coup trouvé dans le livre d'ouvertures.")
            return book_move

        legal_moves = list(board.legal_moves)
        if not legal_moves: return None
            
        best_move = legal_moves[0]
        depth = 1

        while time.time() - self.start_time < self.time_limit and depth < 50:
            self.alpha_beta(board, depth, -float('inf'), float('inf'))
            if not self.abort_search:
                board_hash = chess.polyglot.zobrist_hash(board)
                if board_hash in self.transposition_table:
                    extracted_move = self.transposition_table[board_hash]['move']
                    if extracted_move: best_move = extracted_move
                depth += 1
            else:
                break
        return best_move

# ==============================================================================
# 5. GESTION DE L'API LICHESS
# ==============================================================================
headers = {'Authorization': f'Bearer {montoken}'}
is_playing = False  # Drapeau global pour empêcher deux parties simultanées

def send_pm(username, message):
    """Envoie un message privé à un utilisateur sur Lichess."""
    url = f"https://lichess.org/api/inbox/{username}"
    try: requests.post(url, headers=headers, data={'text': message})
    except Exception as e: print(f"Erreur envoi PM: {e}")

def handle_game(game_id, color):
    """Gère le déroulement d'une partie dans un thread séparé."""
    global is_playing
    is_playing = True
    print(f"[PARTIE] Début de la partie {game_id} avec la couleur {color}")
    
    engine = ChessEngine()
    board = chess.Board()
    url = f"https://lichess.org/api/bot/game/stream/{game_id}"
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        for line in response.iter_lines():
            if not line: continue
            event = json.loads(line.decode('utf-8'))
            
            state = None
            if event.get('type') == 'gameFull':
                state = event['state']
            elif event.get('type') == 'gameState':
                state = event
                
            if state:
                # Vérifier si la partie est terminée
                if state.get('status') != 'started':
                    print(f"[PARTIE] Partie {game_id} terminée. Statut : {state.get('status')}")
                    break
                
                # Reconstruire le plateau avec les coups joués
                board = chess.Board()
                moves_str = state.get('moves', '').strip()
                if moves_str:
                    for m in moves_str.split():
                        board.push_uci(m)
                
                # Est-ce notre tour ?
                is_white_turn = board.turn == chess.WHITE
                if (is_white_turn and color == 'white') or (not is_white_turn and color == 'black'):
                    # Récupérer et convertir notre temps restant (fourni en millisecondes)
                    my_time = state.get('wtime' if color == 'white' else 'btime', 10000) / 1000.0
                    my_inc = state.get('winc' if color == 'white' else 'binc', 10000) / 1000.0
                    
                    # Allocation dynamique intelligente du temps de calcul
                    # On utilise l'incrément et une fraction du temps restant sans jamais vider la pendule
                    allocated_time = (my_time / 22.0) + (my_inc * 0.7)
                    engine.time_limit = max(1.0, min(allocated_time, my_time - 1.0, 8.0))
                    
                    # Calcul du meilleur coup
                    best_move = engine.search_best_move(board)
                    if best_move:
                        move_url = f"https://lichess.org/api/bot/game/{game_id}/move/{best_move.uci()}"
                        requests.post(move_url, headers=headers)
                        print(f"[BOT] Coup joué : {best_move.uci()} (temps alloué : {engine.time_limit:.2f}s)")
                        
    except Exception as e:
        print(f"Erreur pendant la partie : {e}")
    finally:
        is_playing = False

def main_event_loop():
    """Boucle principale qui écoute les flux d'événements Lichess (défis et débuts de parties)."""
    url = "https://lichess.org/api/stream/event"
    
    while True:  # <-- La boucle infinie pour garantir que le bot reste en vie
        print("[CONNEXION] Tentative de connexion au flux d'événements Lichess...")
        
        try:
            response = requests.get(url, headers=headers, stream=True)
            
            # Vérification très importante : Lichess a-t-il accepté notre token ?
            if response.status_code != 200:
                print(f"[ERREUR FATALE] Lichess a refusé la connexion (Code {response.status_code}).")
                print(f"Message de Lichess : {response.text}")
                print("Vérifiez votre token et ses permissions (scopes).")
                time.sleep(10)
                continue # On attend et on réessaie

            print("[SUCCÈS] Connecté au flux ! Le bot est maintenant EN LIGNE.")
            
            for line in response.iter_lines():
                if not line: continue
                event = json.loads(line.decode('utf-8'))
                
                # --- 1. GESTION DES DÉFIS ENTRANTS ---
                if event.get('type') == 'challenge':
                    challenge = event['challenge']
                    challenge_id = challenge['id']
                    challenger = challenge['challenger']['id']
                    variant = challenge['variant']['key']
                    time_control = challenge['timeControl']
                    
                    if is_playing:
                        print(f"[DÉFI] Refusé à {challenger} (Bot actuellement occupé).")
                        requests.post(f"https://lichess.org/api/challenge/{challenge_id}/decline", headers=headers, data={'reason': 'generic'})
                        continue
                    
                    if variant != 'standard':
                        print(f"[DÉFI] Refusé à {challenger} (Variante '{variant}' non supportée).")
                        send_pm(challenger, "Please try standard chess.")
                        requests.post(f"https://lichess.org/api/challenge/{challenge_id}/decline", headers=headers, data={'reason': 'variant'})
                        continue
                    
                    if time_control['type'] != 'clock':
                        print(f"[DÉFI] Refusé à {challenger} (Pas de cadence de temps définie).")
                        send_pm(challenger, "Please use a timed game.")
                        requests.post(f"https://lichess.org/api/challenge/{challenge_id}/decline", headers=headers, data={'reason': 'timeControl'})
                        continue
                        
                    base_time = time_control.get('limit', 0)
                    increment = time_control.get('increment', 0)
                    
                    if base_time < 1 or increment < 10:
                        print(f"[DÉFI] Refusé à {challenger} (Cadence {base_time}+{increment} trop rapide).")
                        send_pm(challenger, "Time control too fast. Need at least 10s increment.")
                        requests.post(f"https://lichess.org/api/challenge/{challenge_id}/decline", headers=headers, data={'reason': 'timeControl'})
                    else:
                        print(f"[DÉFI] Accepté de {challenger} (Cadence: {base_time}+{increment}).")
                        requests.post(f"https://lichess.org/api/challenge/{challenge_id}/accept", headers=headers)

                # --- 2. LANCEMENT DE LA PARTIE ---
                elif event.get('type') == 'gameStart':
                    game_id = event['game']['id']
                    color = event['game']['color']
                    t = threading.Thread(target=handle_game, args=(game_id, color))
                    t.start()
                    
        except Exception as e:
            print(f"[ERREUR CRITIQUE] Perte de connexion : {e}")
            
        print("[DÉCONNEXION] Le flux s'est arrêté. Reconnexion dans 5 secondes...")
        time.sleep(5)

if __name__ == "__main__":
    if montoken == "VOTRE_TOKEN_ICI":
        print("ATTENTION : Veuillez insérer votre token d'API Lichess dans la variable 'montoken' !")
    else:
        main_event_loop()
