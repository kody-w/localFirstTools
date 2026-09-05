import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest


TESTS = Path(__file__).resolve().parent


def load_tests(name):
    spec = importlib.util.spec_from_file_location(name, TESTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('old,new,test_name', [
    (
        'activeWorld = world;\n    resetMovement();',
        'activeWorld = world;',
        'test_return_clears_movement_and_pushes_away_before_resuming',
    ),
    (
        'if (portal && controller.position) {',
        'if (false) {',
        'test_return_clears_movement_and_pushes_away_before_resuming',
    ),
    (
        'const isCurrent = () => activeWorld === world && worldLoadId === loadId;',
        'const isCurrent = () => true;',
        'test_cancelled_load_cannot_replace_the_next_world',
    ),
    (
        'if (!response.ok) {',
        'if (false) {',
        'test_http_errors_are_retryable_and_stale_frames_stay_cancelled',
    ),
    (
        ', 20000);',
        ', 30000);',
        'test_slow_loads_time_out_without_late_reopening',
    ),
    (
        "if (e.target instanceof Element && e.target.closest('input, textarea, select, button, a, [contenteditable]')) return;",
        '',
        'test_typing_focus_loss_and_picker_do_not_leave_movement_stuck',
    ),
    (
        'if (activeWorld || document.hidden) return;',
        '',
        'test_hidden_hub_does_not_render_behind_active_world',
    ),
    (
        'if (worldDocument && worldDocument.pointerLockElement) worldDocument.exitPointerLock();',
        '',
        'test_return_releases_pointer_lock_owned_by_the_child_document',
    ),
    (
        "if (!idoc && (url.protocol === 'http:' || url.protocol === 'https:')) {",
        'if (false) {',
        'test_failed_get_after_successful_head_keeps_retry_and_escape_available',
    ),
    (
        'if (navigation && navigation.responseStatus >= 400) {',
        'if (false) {',
        'test_actual_get_status_is_checked_even_when_the_error_document_contains_a_canvas',
    ),
    (
        "if (!idoc.querySelector('canvas')) {",
        'if (false) {',
        'test_loaded_non_world_html_is_not_promoted_to_ready',
    ),
])
def test_hub_regressions_reject_controlled_mutations(monkeypatch, old, new, test_name):
    module = load_tests('test_portal_hub')
    check = getattr(module, test_name)
    check()
    assert module.SOURCE.count(old) == 1, 'Mutation must target exactly one implementation site'
    monkeypatch.setattr(module, 'SOURCE', module.SOURCE.replace(old, new, 1))
    with pytest.raises(AssertionError, match='ERR_ASSERTION'):
        check()


@pytest.mark.parametrize('old,new,count,test_name', [
    (
        'new Vec3(0, 1, 0)',
        'new Vec3(0, 1, 20)',
        2,
        'test_player_starts_and_respawns_on_the_safe_platform',
    ),
    (
        'const depth = y * sinX - z * cosX;',
        'const depth = y * sinX + z * cosX;',
        1,
        'test_forward_movement_agrees_with_camera_projection',
    ),
    (
        'this.player.pos.add(this.player.vel.mul(dt))',
        'this.player.pos.add(this.player.vel)',
        1,
        'test_jump_physics_are_consistent_at_different_frame_rates',
    ),
    (
        'if (this.animationId === null) this.gameLoop();',
        'this.gameLoop();',
        1,
        'test_resume_and_restart_never_create_duplicate_animation_loops',
    ),
    (
        "if (!this.running || this.paused ||\n                        e.target?.closest?.('button, input, textarea, select, a, [contenteditable]')) return;",
        'if (!this.running || this.paused) return;',
        1,
        'test_space_preserves_native_button_activation_instead_of_jumping',
    ),
    (
        'if (!this.running) return;',
        '',
        1,
        'test_early_and_finished_game_escape_never_hides_the_stopped_menu',
    ),
    (
        "window.addEventListener('blur', () => { this.keys = {}; });",
        '',
        1,
        'test_focus_loss_and_released_pointer_lock_clear_movement',
    ),
    (
        "this.showNotification('Saved statistics are unavailable. You can still start an expedition.');",
        'throw error;',
        1,
        'test_corrupt_statistics_do_not_prevent_start_or_erase_valid_legacy_scores',
    ),
])
def test_dying_star_regressions_reject_controlled_mutations(monkeypatch, old, new, count, test_name):
    module = load_tests('test_dying_star')
    check = getattr(module, test_name)
    check()
    source = module.PAGE.read_text(encoding='utf-8')
    assert source.count(old) == count, 'Mutation sites changed; update the measurement'
    mutated = source.replace(old, new)
    monkeypatch.setattr(module, 'PAGE', SimpleNamespace(read_text=lambda **kwargs: mutated))
    with pytest.raises(AssertionError, match='ERR_ASSERTION'):
        check()


def test_destination_check_rejects_a_missing_portal():
    module = load_tests('test_portal_hub')
    module.test_portal_points_to_a_real_world_under_both_host_roots(*module.WORLDS[0])
    with pytest.raises(AssertionError, match='missing-portal'):
        module.test_portal_points_to_a_real_world_under_both_host_roots(
            'missing-portal', 'missing-portal-gate.html',
        )


@pytest.mark.parametrize('old,new,test_name', [
    (
        'this.camera.updateProjectionMatrix();',
        '',
        'test_camera_resize_updates_projection_and_caps_pixel_ratio',
    ),
    (
        'new SphereGeometry(1, 8, 8)',
        'new SphereGeometry(0, 8, 8)',
        'test_generated_plants_are_on_island_surfaces_with_unit_geometry',
    ),
    (
        'this.player.seeds = state.player.seeds;',
        'this.player.seeds = state.player.seeds || 10;',
        'test_json_and_local_save_roundtrip_preserve_layout_colors_and_metadata',
    ),
])
def test_garden_regressions_reject_controlled_mutations(monkeypatch, old, new, test_name):
    module = load_tests('test_quantum_garden')
    check = getattr(module, test_name)
    check()
    assert module.SCRIPT.count(old) == 1, 'Mutation must target one garden implementation site'
    monkeypatch.setattr(module, 'SCRIPT', module.SCRIPT.replace(old, new, 1))
    with pytest.raises(AssertionError, match='ERR_ASSERTION'):
        check()
