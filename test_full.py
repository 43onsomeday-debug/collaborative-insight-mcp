"""
   
Collaborative Insight Generation Framework - All Phases
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from phases import (
    RequestAnalyzer,
    ExpertAssigner,
    InformationGatherer,
    Clarifier,
    DesignGenerator,
    LLMSelector,
    Executor,
    Validator
)


async def test_full_pipeline():
    """   """
    
    print("=" * 70)
    print("Collaborative Insight Generation Framework")
    print(" Phase   (Phase 0-7)")
    print("=" * 70)
    
    #  
    user_request = """
         .
            ,
           .
        .
    """
    
    print(f"\n  :")
    print(f"{user_request.strip()}")
    print()
    
    # =========================================================================
    # Phase 0:  
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 0:    ")
    print("=" * 70)
    
    phase0_result = RequestAnalyzer.analyze(user_request)
    
    print(f"\n  :")
    print(f"    : {phase0_result.request_type.value}")
    print(f"    : {phase0_result.clarity_score.total_score}/5")
    if phase0_result.complexity_score:
        print(f"    : {phase0_result.complexity_score.total_score}/7")
    print(f"   : {phase0_result.confidence}")
    print(f"    : {phase0_result.reasoning}")
    
    # =========================================================================
    # Phase 1:  
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 1:      ")
    print("=" * 70)
    
    complexity = phase0_result.complexity_score.total_score if phase0_result.complexity_score else 0
    phase1_result = ExpertAssigner.assign(user_request, complexity)
    
    print(f"\n   :")
    print(f"\n   :")
    print(f"    Domain    : {phase1_result.hierarchy.domain}")
    print(f"    Subdomain : {phase1_result.hierarchy.subdomain}")
    print(f"    Category  : {phase1_result.hierarchy.category}")
    print(f"    Task      : {phase1_result.hierarchy.task}")
    
    print(f"\n    ({len(phase1_result.experts)}):")
    for i, expert in enumerate(phase1_result.experts, 1):
        print(f"    {i}. {expert.name}")
        print(f"       : {expert.expertise}")
        print(f"       : {[layer.value for layer in expert.layers]}")
    
    print(f"\n   : {phase1_result.processing_mode.value}")
    
    # =========================================================================
    # Phase 2:  
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 2:   ")
    print("=" * 70)
    
    expert_names = [e.name for e in phase1_result.experts]
    phase2_result = await InformationGatherer.gather_information(
        user_request,
        expert_names
    )
    
    print(f"\n   :")
    print(f"    : {len(phase2_result.research_items)}")
    print(f"    : {len(phase2_result.sources)}")
    print(f"\n   5  :")
    for i, item in enumerate(phase2_result.research_items[:5], 1):
        print(f"    {i}. {item.query}")
        print(f"       : {item.category}, : {item.priority}")
    
    # =========================================================================
    # Phase 3: 
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 3:  ")
    print("=" * 70)
    
    clarity_score = phase0_result.clarity_score.total_score
    phase3_result = Clarifier.generate_questions(
        user_request,
        clarity_score
    )
    
    print(f"\n   :")
    print(f"    : {'' if phase3_result.clarification_needed else ''}")
    print(f"    : {len(phase3_result.questions)}")
    
    if phase3_result.questions:
        print(f"\n   :")
        for i, q in enumerate(phase3_result.questions, 1):
            print(f"    {i}. [{q.category}] {q.question}")
    else:
        print(f"         .")
    
    # =========================================================================
    # Phase 4:   
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 4:   ")
    print("=" * 70)
    
    phase4_result = await DesignGenerator.create_design(
        user_request,
        phase0_result,
        phase1_result
    )
    
    design_doc = phase4_result.design_document
    
    print(f"\n   :")
    print(f"   : {design_doc.title}")
    print(f"    : {design_doc.quality_level.value}")
    print(f"   : {design_doc.version}")
    print(f"    : {len(design_doc.sections)}")
    
    print(f"\n   :")
    for i, section in enumerate(design_doc.sections, 1):
        print(f"    {i}. {section.section_name}")
        content_preview = section.content[:80] + "..." if len(section.content) > 80 else section.content
        print(f"       {content_preview}")
    
    # =========================================================================
    # Phase 5: LLM 
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 5: LLM ")
    print("=" * 70)
    
    phase5_result = LLMSelector.select_models(
        design_doc,
        complexity
    )
    
    print(f"\n LLM  :")
    print(f"    : {len(phase5_result.selections)}")
    
    for i, selection in enumerate(phase5_result.selections, 1):
        print(f"\n    {i}. {selection.model_id}")
        print(f"       Provider : {selection.provider}")
        print(f"       Role     : {selection.role}")
        print(f"       Confidence: {selection.confidence:.2f}")
        if selection.capabilities:
            caps = [cap.value for cap in selection.capabilities]
            print(f"       Capabilities: {', '.join(caps)}")
    
    # =========================================================================
    # Phase 6: 
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 6: ")
    print("=" * 70)
    
    phase6_result = await Executor.execute(
        phase5_result,
        design_doc
    )
    
    print(f"\n  :")
    print(f"   : {phase6_result.status}")
    print(f"    : {phase6_result.execution_time:.2f}")
    
    result_preview = str(phase6_result.result)[:200] + "..." if len(str(phase6_result.result)) > 200 else str(phase6_result.result)
    print(f"\n   :")
    print(f"  {result_preview}")
    
    # =========================================================================
    # Phase 7: 
    # =========================================================================
    print("\n" + "=" * 70)
    print("Phase 7:    ")
    print("=" * 70)
    
    phase7_result = Validator.validate_result(
        phase6_result.result,
        user_request,
        design_doc
    )
    
    validation = phase7_result.validation_result
    metrics = phase7_result.quality_metrics
    
    print(f"\n  :")
    print(f"    : {'' if validation.passed else ''}")
    print(f"   : {validation.severity}")
    
    print(f"\n   :")
    print(f"       : {metrics.overall_score:.2f}")
    print(f"        : {metrics.completeness:.2f}")
    print(f"        : {metrics.accuracy:.2f}")
    print(f"        : {metrics.consistency:.2f}")
    print(f"        : {metrics.usability:.2f}")
    print(f"        : {metrics.confidence:.2f}")
    
    print(f"\n   :")
    for check in validation.checks:
        status = "" if check.passed else ""
        print(f"    [{status}] {check.check_name}: {check.score:.2f} ({check.level.value})")
        if check.issues:
            for issue in check.issues:
                print(f"          {issue}")
    
    if phase7_result.improvements:
        print(f"\n   :")
        for i, suggestion in enumerate(phase7_result.improvements, 1):
            print(f"    {i}. {suggestion}")
    
    # =========================================================================
    #  
    # =========================================================================
    print("\n" + "=" * 70)
    print(" ")
    print("=" * 70)
    
    print(f"""
   Phase 0:   - {phase0_result.request_type.value} (: {phase0_result.clarity_score.total_score}/5)
   Phase 1:   - {len(phase1_result.experts)} 
   Phase 2:   - {len(phase2_result.sources)}  
   Phase 3:  - {len(phase3_result.questions)}  {'' if phase3_result.questions else '()'}
   Phase 4:   - {len(design_doc.sections)}  ({design_doc.quality_level.value})
   Phase 5: LLM  - {phase5_result.selections[0].model_id}
   Phase 6:  - {phase6_result.status} ({phase6_result.execution_time:.2f})
   Phase 7:  - {'' if validation.passed else ''} (: {metrics.overall_score:.2f})
    """)
    
    print("=" * 70)
    print("    !")
    print("=" * 70)


async def test_simple_request():
    """  """
    
    print("\n\n" + "=" * 70)
    print(" :  ")
    print("=" * 70)
    
    simple_request = "Python    "
    
    print(f"\n: {simple_request}")
    
    # Phase 0 
    result = RequestAnalyzer.analyze(simple_request)
    print(f"\n :")
    print(f"  : {result.request_type.value}")
    print(f"  : {result.clarity_score.total_score}/5")
    print(f"  : {result.complexity_score.total_score if result.complexity_score else 'N/A'}")


if __name__ == "__main__":
    #   
    asyncio.run(test_full_pipeline())
    
    #   
    asyncio.run(test_simple_request())

